# This is a simplified rewrite of the FlagSet 
# utility class core functionality, for the purpose 
# of being transpiled into JS using javascripthon.
# As such, the following Python language features
# should be avoided:
#  - imports
#  - named built-in methods of objects
# Access to more advanced features should be provided
# through the lib object passed to FlagSetCore.

class FlagSetCore:
    # flagspec is a dictionary object that is generated
    #   by compile_flags.py for both Python and JS, and
    #   must be passed to the object on creation since
    #   they are not part of this transpiled file.
    # lib is an object exposing various utility functions,
    #   in order to abstract away that they cannot be
    #   transpiled directly:
    #     b64encode(array_of_byte_values)
    #     b64decode(string)
    #     re_test(expression, string)
    #       -> returns true/false
    #     re_search(expression, string)
    #       -> returns list of match groups, or null if no match
    #     re_sub(expression, replacement, string)
    #     push(list, value)
    #     remove(list, value)
    #     join(list, separator)
    #     min(a, b)
    #     is_string(obj)
    #     keys(dict)
    def __init__(self, flagspec, lib):
        self._flagspec = flagspec
        self._lib = lib
        self._flags = {}
        self._embedded_version = None

    def load(self, flag_string):
        if len(flag_string) > 0 and flag_string[0] == 'b':
            self._load_binary(flag_string)
        else:
            self._load_text(flag_string)

    def _load_text(self, flag_string):
        self._flags = {}
        self._embedded_version = None
        index = 0
        superflag = None
        flag_string = self._lib.re_sub(r'\s', '', flag_string)

        while len(flag_string) > 0:
            m = self._lib.re_search(r'^[A-Z]', flag_string)
            if m:
                superflag = m[0]
                flag_string = flag_string[len(superflag):]
                continue

            m = self._lib.re_search(r'^-[a-z0-9_]+:?', flag_string)
            if m:
                superflag = m[0]
                flag_string = flag_string[len(superflag):]
                if not self._lib.re_test(r'\:$', superflag):
                    self.set(superflag)
                continue

            m = self._lib.re_search(r'^([a-z0-9_]+:)?([a-z0-9_]+(,[a-z0-9_]+)*)/?', flag_string)
            if m:
                if superflag is None:
                    raise Exception(f"Parse error: found subflag without superflag around '{m[0]}'")
                subflag_prefix = (m[1] if m[1] else '')
                subflags = m[2].split(',')
                for i in range(len(subflags)):
                    self.set(superflag + subflag_prefix + subflags[i])
                flag_string = flag_string[len(m[0]):]
                continue

            raise Exception(f"Parse error around '{flag_string}'")


    def _load_binary(self, binary_string):
        binary_string = binary_string[1:] # remove starting 'b'
        byte_list = self._lib.b64decode(binary_string)
        if len(byte_list) < 3:
            raise Exception("Binary flag string too short")
        self._embedded_version = byte_list[:3]
        for i in range(3):
            if self._embedded_version[i] != self._flagspec['version'][i]:
                embedded_version_string = self._lib.join([str(v) for v in embedded_version_string], '.')
                spec_version_string = self._lib.join([str(v) for v in self._flagspec['version']], '.')
                raise Exception(f"Version mismatch: flag string is v{embedded_version_string}, expected v{spec_version_string}")

        byte_list = byte_list[3:]
        
        self._flags = {}
        for i in range(len(self._flagspec['binary'])):
            flag_binary_info = self._flagspec['binary'][i]

            field_size = flag_binary_info['size']
            byte_index = (flag_binary_info['offset'] >> 3)
            bit_index = (flag_binary_info['offset'] & 0x7)

            value = 0
            value_bit_index = 0
            while (field_size > 0):
                subfield_size = self._lib.min(field_size, 8 - bit_index)
                src_byte = (byte_list[byte_index] if byte_index < len(byte_list) else 0)
                value = value | (((src_byte >> bit_index) & ((1 << subfield_size) - 1)) << value_bit_index)
                value_bit_index += subfield_size
                field_size -= subfield_size
                byte_index += 1
                bit_index = 0

            if value == flag_binary_info['value']:
                self.set(flag_binary_info['flag'])

    def get_list(self, regex=None):
        flags = []
        for flag in self._flagspec['order']:
            if self.has(flag):
                if regex is None or self._lib.re_test(regex, flag):
                    self._lib.push(flags, flag)
        return flags

    def get_suffix(self, flag_prefix):
        flag_regex = '^' + flag_prefix
        flags = self.get_list(flag_regex)
        if len(flags) > 0:
            return flags[0][len(flag_prefix):]
        else:
            return None

    def get_version(self):
        return self._embedded_version
        
    def has(self, flag):
        if flag not in self._flagspec['order']:
            raise Exception(f"Invalid flag {flag}")

        if flag in self._flagspec['implicit']:
            return self._evaluate_condition(self._flagspec['implicit'][flag])
        elif flag in self._flags:
            return True
        else:
            return False

    def has_any(self, *flags):
        for flag in flags:
            if self.has(flag):
                return True
        return False

    def has_all(self, *flags):
        for flag in flags:
            if not self.has(flag):
                return False
        return True

    def set(self, flag):
        if flag in self._flagspec['implicit']:
            # Cannot set implicit flags
            return

        for mutex_set in self._flagspec['mutex']:
            if flag in mutex_set:
                for other_flag in mutex_set:
                    if other_flag != flag:
                        self.unset(other_flag)
                break

        self._flags[flag] = True

    def unset(self, flag):
        if flag in self._flags:
            del self._flags[flag]

    def parse(self):
        results = []
        for flag in self._flagspec['order']:
            if not self.has(flag):
                continue

            if flag[0] == '-':
                m = self._lib.re_search(r'^(-[a-z0-9_]+:?)([a-z0-9_]+)?$', flag)
                superflag = m[1]
                subflag = m[2]
                subsubflag = None
            else:
                m = self._lib.re_search(r'^([A-Z])(([a-z0-9_]+:)?([a-z0-9_]+))?$', flag)
                superflag = m[1]
                subflag = (m[3] if m[3] else m[4])
                subsubflag = (m[4] if m[3] else None)

            superflag_obj = None
            for item in results:
                if item[0] == superflag:
                    superflag_obj = item
                    break
            if not superflag_obj:
                superflag_obj = [superflag, []]
                self._lib.push(results, superflag_obj)

            if subflag:
                subflag_obj = None
                for item in superflag_obj[1]:
                    if item[0] == subflag:
                        subflag_obj = item
                        break
                if not subflag_obj:
                    subflag_obj = [subflag, []]
                    self._lib.push(superflag_obj[1], subflag_obj)

                if subsubflag:
                    self._lib.push(subflag_obj[1], subsubflag)

        return results

    def _evaluate_condition(self, condition):
        if self._lib.is_string(condition):
            return self.has(condition)
        elif condition[0] == 'not':
            return not self._evaluate_condition(condition[1])
        elif condition[0] == 'and':
            for subcondition in condition[1:]:
                if not self._evaluate_condition(subcondition):
                    return False
            return True
        elif condition[0] == 'or':
            for subcondition in condition[1:]:
                if self._evaluate_condition(subcondition):
                    return True
            return False
        else:
            raise Exception(f"Unsupported condition type {condition[0]}")

    def _wrap(self, text, first_line_width, paragraph_width):
        line_width = first_line_width
        lines = []
        while len(text) > line_width:
            break_index = line_width
            for i in range(line_width - 1, -1, -1):
                if text[i] == ',' or text[i] == ')' or text[i] == ' ':
                    break_index = i + 1
                    break

            self._lib.push(lines, text[:break_index])
            text = text[break_index:]
            line_width = paragraph_width

        if len(text) > 0:
            self._lib.push(lines, text)

        return lines


    def to_string(self, pretty=False, wrap_width=None):
        parsed = self.parse()

        # in pretty mode, parts is the components of the current line being built
        # in not pretty mode, parts is the components of the full complete string
        parts = []

        # in pretty mode, as parts is converted into lines, they are added here
        lines = []

        last_superflag = None
        for superflag_obj in parsed:
            if not pretty and len(parts) > 0:
                self._lib.push(parts, ' ')
            elif pretty and len(lines) > 0 and last_superflag[0] != '-':
                self._lib.push(lines, '')

            superflag = superflag_obj[0]
            last_superflag = superflag
            superflag_last_index = len(superflag) - 1 # needed to workaround https://github.com/metapensiero/metapensiero.pj/issues/78
            superflag_prefix = superflag + (' ' if pretty and superflag[superflag_last_index] != ':' else '')
            self._lib.push(parts, superflag_prefix)

            if len(superflag_obj[1]) > 0:
                if superflag[0] == '-':
                    # for subflags of -switch style flags, we want them to be
                    # rendered in one comma-separated parentheses, so create
                    # an object with a blank subflag and with the original subflag
                    # list as subsubflags
                    subsubflags = []
                    for subflag_obj in superflag_obj[1]:
                        self._lib.push(subsubflags, subflag_obj[0])
                    subflag_obj_list = [ ['', subsubflags] ]
                else:
                    subflag_obj_list = superflag_obj[1]

                subflag_obj_index = 0
                for subflag_obj in subflag_obj_list:
                    if pretty and len(parts) == 0:
                        # indent new line
                        self._lib.push(parts, ' /')

                    segment = subflag_obj[0] + self._lib.join(subflag_obj[1], ',')
                    if pretty:
                        self._lib.push(parts, segment)
                        paragraph_indent = '   '
                        line = self._lib.join(parts, '')
                        if wrap_width is None:
                            sublines = [line]
                        else:
                            sublines = self._wrap(line, wrap_width, wrap_width - len(paragraph_indent))

                        prefix = ''
                        for subline in sublines:
                            self._lib.push(lines, prefix + subline)
                            prefix = paragraph_indent

                        parts = []
                    else:
                        if subflag_obj_index > 0:
                            self._lib.push(parts, '/')
                        self._lib.push(parts, segment)

                    subflag_obj_index += 1

            elif pretty:
                self._lib.push(lines, parts[0])
                parts = []

        if not pretty:
            line = self._lib.join(parts, '')
            if wrap_width is not None:
                line = self._lib.join(self._wrap(line, wrap_width, wrap_width), '\n')
            return line
        else:
            return self._lib.join(lines, '\n')


    def to_binary(self):
        byte_list = []
        for i in range(3):
            self._lib.push(byte_list, self._flagspec['version'][i])

        for flag_binary_info in self._flagspec['binary']:
            if not self.has(flag_binary_info['flag']):
                continue

            value = flag_binary_info['value']
            field_size = flag_binary_info['size']
            byte_index = (flag_binary_info['offset'] >> 3) + 3  # +3 to account for version bytes
            bit_index = (flag_binary_info['offset'] & 0x7)
            #print(f"{flag_binary_info['flag']:20} : {value}[{field_size}] @ {flag_binary_info['offset']} -> {byte_index}.{bit_index}")

            while field_size > 0:
                while byte_index >= len(byte_list):
                    self._lib.push(byte_list, 0)

                dst_byte = byte_list[byte_index]
                subfield_size = self._lib.min(field_size, 8 - bit_index)
                subvalue = value & ((1 << subfield_size) - 1)
                #print(f"  Apply {subvalue << bit_index:02X} to byte {byte_index}")
                byte_list[byte_index] = dst_byte | (subvalue << bit_index)

                value >>= subfield_size
                field_size -= subfield_size
                bit_index = 0
                byte_index += 1

        return 'b' + self._lib.b64encode(byte_list)


#----------------------------------------------------------------------------------------

# This class handles flagset verification and correction.

class FlagLogicCore:
    def __init__(self, flagspec, lib):
        self._flagspec = flagspec
        self._lib = lib

    def _simple_disable(self, flagset, log, prefix, flags_to_disable):
        for flag in flags_to_disable:
            if flagset.has(flag):
                flagset.unset(flag)
                print(prefix + '; removed ' + flag)
                self._lib.push(log, ['correction', prefix + '; removed ' + flag])

    def _simple_disable_regex(self, flagset, log, prefix, flags_regex):
        self._simple_disable(flagset, log, prefix, flagset.get_list(flags_regex))

    # alters the flagset in place
    # returns a list of 2-tuples describing errors found and fixes made:
    #             [ <cleanup | correction | error>, <string describing fix> ]
    def fix(self, flagset):
        log = []

        # NOTE: mutex flags ARE handled internally by FlagSet, don't worry about them here        
        # key item flags
        if flagset.has('-starting:underground'):
            self._simple_disable_regex(flagset, log, 'Starting underground is already unsafe', r'^Kunsafe') # also hits Kunsafer
            self._simple_disable_regex(flagset, log, 'Starting underground already forces the Drill for progression', r'^Kforce:')

        if flagset.has('Kunsafer'):
            # note that if we're starting underground, this check will not occur, so you *can* start with Magma/Hook
            self._simple_disable(flagset, log, 'Cannot start with underground access on Kunsafer', ['Kstart:magma', 'Kstart:hook'])
            
        if flagset.has('Kunsafer') and not flagset.has_any('Ksummon', 'Kmoon', 'Kmiab:above', 'Kmiab:lst', 'Kmiab:standard', 'Kmiab:all'):
            flagset.set('Kmoon')
            self._lib.push(log, ['correction', 'Kunsafer requires placing key items on the moon/Giant, and Knofree does not count; adding Kmoon (but you can instead add any Darkness-locked checks)'])

        if flagset.has('Kforge') and flagset.has('Omode:classicforge'):
            self._simple_disable(flagset, log, 'Classic forge is incompatible with Kforge', ['Kforge'])

        if flagset.has('Kforge'):
            self._simple_disable_regex(flagset, log, '-smith is incompatible with Kforge', r'^-smith:')

        if flagset.has_any('Ksummon', 'Kmoon', 'Kforge', 'Kpink',
                           'Kmiab:standard', 'Kmiab:above', 'Kmiab:below', 'Kmiab:lst',
                           'Kmiab:all') and not flagset.has('Kmain'):
            flagset.set('Kmain')
            self._lib.push(log, ['correction', 'Advanced key item randomizations are enabled; forced to add Kmain'])

        if flagset.has('Owin:crystal') and flagset.has('Omode:ki17'):
            flagset.unset('Omode:ki17')
            flagset.set('Omode:ki16')
            self._lib.push(log, ['correction', 'Can only collect 16 KIs for an objective with Owin:crystal; changing Omode:ki17 to Omode:ki16'])

        if flagset.has('Owin:crystal'):
            self._simple_disable(flagset, log, 'Cannot start with the Crystal if it is the objective reward', ['Kstart:crystal'])

        if not flagset.has_any('Ksummon', 'Kmoon', 'Kforge', 'Kpink',
                           'Kmiab:standard', 'Kmiab:above', 'Kmiab:below', 'Kmiab:lst',
                           'Kmiab:all') and flagset.has('Omode:ki17'):
            self._simple_disable(flagset, log, 'Cannot replace a key item if all of them are required', ['Pkey', 'Kstart:pass'])
            self._simple_disable(flagset, log, 'Cannot remove a key item reward slot if all of them are required', ['Kstart:zonk'])

        if not flagset.has_any('Ksummon', 'Kmoon', 'Kforge', 'Kpink',
                           'Kmiab:standard', 'Kmiab:above', 'Kmiab:below', 'Kmiab:lst',
                           'Kmiab:all') and flagset.has('Pkey') and not flagset.has('Owin:crystal') and flagset.has('Omode:ki16'):
            self._simple_disable(flagset, log, 'Cannot remove two key items if one of them is required', ['Kstart:zonk'])

        if flagset.has('Kvanilla'):
            self._simple_disable(flagset, log, 'Key items not randomized', ['Kunsafe', 'Kunsafer','Kunweighted'])
            self._simple_disable_regex(flagset, log, 'Key items not randomized', r'^Kstart:')        

        if flagset.has('Kstart:darkness'):
            self._simple_disable(flagset, log, 'Klatedark is incompatible with starting with Darkness', ['Klatedark'])

        if flagset.has('Klatedark'):
            self._simple_disable(flagset, log, 'Klatedark implicitly guarantees safe underground access', ['Kunsafe', 'Kunsafer'])

        if flagset.has('Kstart:pass') and not flagset.has('Pkey'):
            flagset.set('Pkey')
            self._lib.push(log, ['correction', 'Kstart:pass implies Pkey'])

        kmiab_flags = flagset.get_list(r'^Kmiab:')
        if 'Kmiab:all' in kmiab_flags and len(kmiab_flags) > 1:
            self._simple_disable_regex(flagset, log, 'All miabs already included', r'^Kmiab:(standard|above|below|lst)')
        elif 'Kmiab:standard' in kmiab_flags and len(kmiab_flags) > 1:
            self._simple_disable_regex(flagset, log, 'Standard miab inclusion takes priority', r'^Kmiab:(above|below|lst)')

        if flagset.has('Cvanilla'):
            self._simple_disable_regex(flagset, log, 'Characters not randomized', r'^C(maybe|distinct:|only:|no:)')
        else:
            only_flags = flagset.get_list(r'^Conly:')
            if len(only_flags) > 0:
                self._simple_disable_regex(flagset, log, 'Conly:* flag(s) are specified', r'^Cno:')

        if flagset.has_any('Chero', 'Csuperhero'):
            # note: it's fine to keep -smith:good, to make sure the weapon is strong, and -smith:spoilsuper, for preview fun
            self._simple_disable_regex(flagset, log, 'Hero challenge includes smith weapon', r'^-smith:(super|alt|playable)')
            if flagset.has('Aagnostic'):
                flagset.set('Ahero')
                self._lib.push(log, ['correction', 'In the absence of other agility flags, any hero challenge implies Ahero; replaced Aagnostic with Ahero'])

        start_include_flags = flagset.get_list(r'^Cstart:(?!not_)')
        start_exclude_flags = flagset.get_list(r'^Cstart:not_')
        if len(start_exclude_flags) > 0 and len(start_include_flags) > 0:
            self._simple_disable_regex(flagset, log, 'Inclusive Cstart:* flags are specified', r'^Cstart:not_')
        if len(start_include_flags) > 1 and flagset.has('Cstart:any'):
            self._simple_disable_regex(flagset, log, 'Cstart:any is specified', r'^Cstart:(?!any|not_)')

        if flagset.has('Kstart:magma') and flagset.has('Kforce:hook'):
            self._simple_disable_regex(flagset, log, 'Force hook with start:Magma', r'^Kforce:hook')

        if flagset.has('Cnekkie') and len(flagset.get_list(r'^Cthrift:')) > 0:
            self._simple_disable_regex(flagset, log, 'Starting gear specified by Cnekkie', r'^Cthrift:')

        if  (flagset.has('Ctreasure:unsafe') or flagset.has('Ctreasure:relaxed')) and not (flagset.has('Ctreasure:free') or flagset.has('Ctreasure:earned')):
            flagset.set('Ctreasure:free')
            flagset.set('Ctreasure:earned')
            self._lib.push(log, ['correction', 'Ctreasure:unsafe/wild set, auto-assigning Ctreasure:free and Ctreasure:earned'])            

        if flagset.get_list(r'^Ctreasure:') and (flagset.has('Tvanilla') or flagset.has('Tshuffle') or flagset.has('Tempty')):
            self._simple_disable_regex(flagset, log, 'Ctreasure: with vanilla, shuffled, or empty chests', r'^Ctreasure:')

        if flagset.has('Ctreasure:earned') and not flagset.has('Cnoearned'):                            
            flagset.set('Cnoearned')
            self._lib.push(log, ['correction', 'Ctreasure:earned set, auto-assigning Cnoearned'])
        
        if flagset.has('Ctreasure:free') and not flagset.has('Cnofree'):                    
            flagset.set('Cnofree')
            self._lib.push(log, ['correction', 'Ctreasure:free set, auto-assigning Cnofree'])        

        if flagset.has('Tempty'):
            self._simple_disable_regex(flagset, log, 'Treasures are empty', r'^Tsparse:')

        if flagset.get_list(r'^Tsparsey:') and not flagset.get_list(r'^Tsparse:'):
            self._simple_disable_regex(flagset, log, 'Tsparsey specified without Tsparse', r'^Tsparsey:')            

        if flagset.has_any('Tempty', 'Tvanilla', 'Tshuffle'):
            self._simple_disable_regex(flagset, log, 'Treasures are not random', r'^Tmaxtier:')
            self._simple_disable_regex(flagset, log, 'Treasures are not random', r'^Tmintier:')

        mintier_flags = flagset.get_list(r'^Tmintier:')
        maxtier_flags = flagset.get_list(r'^Tmaxtier:')
        if len(mintier_flags) > 0 and len(maxtier_flags) > 0:
            mintier = int(self._lib.re_sub(r'^Tmintier:', '', mintier_flags[0]))
            maxtier = int(self._lib.re_sub(r'^Tmaxtier:', '', maxtier_flags[0]))
            if maxtier < mintier:
                flagset.unset(mintier_flags[0])
                flagset.set('Tmintier:' + f'{maxtier}')
                self._lib.push(log, ['correction', f'Tmaxtier cannot be less than Tmintier, so replacing Tmintier:{mintier} with Tmintier:{maxtier}'])

        if flagset.has('Tadjmiabareas') and not flagset.has_any('Tpro', 'Tsemipro', 'Twildish', 'Tvanillaish', 'Tstandardish'):
            self._simple_disable(flagset, log, 'Treasures are not weighted', ['Tadjmiabareas'])

        if flagset.has_any('Svanilla', 'Sshuffle', 'Scabins', 'Sempty'):
            self._simple_disable_regex(flagset, log, 'Shops are not random', r'^(Sno:([^j]|j.)|Salways:([^j]|j.))')
            if not flagset.has('Sshuffle'):
                self._simple_disable(flagset, log, 'Shops are not random', ['Sunsafe'])

        for f in ['apples', 'sirens', 'vampires', 'hrglass', 'bacchus', 'starveil', 'cure3', 'illusion', 'coffin', 'damage_items']:
            if flagset.has('Salways:' + f) and flagset.has('Sno:' + f):
                self._simple_disable(flagset, log, 'Salways: overrides Sno:', ['Sno:' + f])

        if flagset.has('Bvanilla'):
            self._simple_disable(flagset, log, 'Bosses not randomized', ['Bunsafe', 'Bzones'])

        if flagset.has('Evanilla'):
            self._simple_disable(flagset, log, 'Encounters are vanilla', ['Ekeep:behemoths', 'Ekeep:doors', 'Edanger'])

        if len(flagset.get_list(r'^-smith:(playable|good)')) == len(flagset.get_list(r'^-smith:')):
            self._simple_disable(flagset, log, 'No smith item requested', ['-smith:playable', '-smith:good'])
        if flagset.has_any('-smith:omni', '-smith:spoilsuper', '-smith:sellsuper') and not (flagset.has_any('-smith:super', 'Chero', 'Csuperhero')):
            self._simple_disable(flagset, log, 'No FF4A weapon available', ['-smith:omni', '-smith:spoilsuper', '-smith:sellsuper'])

        # add restrictions in case people try to fudge the fusoya flags
        if flagset.has('Fslowstart') and flagset.has('Funcapped'):
            self._simple_disable(flagset, log, 'Uncapped FuSoYa cannot also have slowstart', ['Fslowstart'])
        if flagset.has('Flocation') and flagset.has('Fslowstart'):
            self._simple_disable(flagset, log, 'Location FuSoYa cannot have slowstart', ['Fslowstart'])
        if flagset.has('Fnerfed'):
            self._simple_disable_regex(flagset, log, 'Nerfed FuSoYa cannot have slowstart or unlearn spells', r'^F(slowstart|unlearn)')
        if flagset.has('Fvanilla'):
            self._simple_disable_regex(flagset, log, 'Vanilla FuSoYa cannot have his HP or spells change', r'^F(slowstart|unlearn|randomhp)')

        if flagset.has('-monsterflee') and not flagset.has('-monsterevade'):
            flagset.set('-monsterevade')
            self._lib.push(log, ['correction', 'Monsters require evade to flee; forced to add -monsterevade'])

        if flagset.has_any('-entrancesrando:normal','-entrancesrando:gated','-entrancesrando:blueplanet','-entrancesrando:why','-entrancesrando:all'):
            self._simple_disable_regex(flagset, log, 'Entrances rando takes priority', r'^-doorsrando')

        # cannot currently do -starting: flags with gated objectives or doors/entrances rando
        gated_objectives = flagset.get_list(r'^Ogated:')
        doors_entrances_rando = flagset.get_list(r'^-(doors|entrances)rando:')
        if (flagset.has_any('-starting:underground','-starting:blackchocobo')
            and (len(gated_objectives) > 0 or len(doors_entrances_rando) > 0)):
            self._lib.push(log, ['error', "Different starting location flags are not currently available in combination with doors/entrances rando or gated objectives; remove them and try again."])

        unsure_flags = flagset.get_list(r'^Zunsure:')
        for fl in unsure_flags:
            fl_cat = 'Z' + self._lib.re_sub(r'^Zunsure:', '', fl)
            if flagset.has(fl_cat):
                flagset.unset(fl)
                self._lib.push(log, ['correction', f'Cannot use {fl} when {fl_cat} is set; removed {fl}'])

        if flagset.has('Zphysical') and flagset.has('Zwhichbang'):
            self._simple_disable(flagset, log, 'No guaranteed Big Bangs in script', ['Zwhichbang'])

        if flagset.has_any('Zchaos', 'Zlavosshell') and not flagset.has_any('Zunsure:vanilla', 'Zunsure:physical', 'Zunsure:ailments'):
            self._simple_disable(flagset, log, 'Random phases take precedence over shuffled phases', ['Zphaseshift'])

        all_spoiler_flags = flagset.get_list(r'^-spoil:')
        sparse_spoiler_flags = flagset.get_list(r'^-spoil:sparse')
        if (len(all_spoiler_flags) > 0 and len(all_spoiler_flags) == len(sparse_spoiler_flags)):
            self._simple_disable_regex(flagset, log, 'No spoilers requested', r'^-spoil:sparse')

        if flagset.has('Chi') and flagset.has_any('Chero', 'Csuperhero') and flagset.has('Cparty:1'):  
            self._simple_disable(flagset, log, 'No room for characters to be added with a hero challenge and Max Party size of 1', ['Chi'])

        if flagset.has('Cfifo') and flagset.has_any('Chero', 'Csuperhero') and flagset.has('Cparty:1'):  
            self._simple_disable(flagset, log, 'Cant remove characters with a hero challenge and Max Party size of 1', ['Cfifo'])

        if flagset.has('Cpermajoin') and flagset.has('Cfifo'):
            self._simple_disable(flagset, log, 'Permajoin and Remove Oldest are incompatible', ['Cfifo'])

        # tweaks are intended to avoid conflicts, but Rydia's Red Mage flag interacts with Dwarf Castle (let her learn a summon at Hobs, why not)
        if flagset.has('-tweak:rydiaredmage'):
            if flagset.has_any('-call:vanillagrowup', '-call:nogrowup'):
                self._simple_disable(flagset, log, 'Rydia must learn white magic at Dwarf Castle as a Red Mage', ['-call:vanillagrowup', '-call:nogrowup'])

        # Objectives logic
        if flagset.has('Onone'):
            self._simple_disable_regex(flagset, log, 'No objectives set', r'^O(win|req):')
            self._simple_disable_regex(flagset, log, 'No objectives set', r'^Xobjectivebonus')
        else:
            # Force Oreq:all if a req: flag is not specified
            if len(flagset.get_list(r'^Oreq:')) == 0:
                flagset.set('Oreq:all')
                self._lib.push(log, ['correction', 'Required number of objectives not specified; setting Oreq:all'])

            hard_required_objectives = flagset.get_list(r'^Ohardreq:')
            if flagset.has('Oreq:all'):                
                if len(hard_required_objectives) != 0:
                    self._simple_disable_regex(flagset, log, 'Hard required objectives found, but all objectives are already required. Removing hard required flags', r'^Ohardreq:')
                    self._lib.push(log, ['correction', 'Hard required objectives found, but all objectives are already required.  Ignoring hard required flags.'])                    
            else:
                required_count = flagset.get_list(r'^Oreq:')
                if len(required_count ) > 0 :
                    required_objective_count = int(self._lib.re_sub(r'^Oreq:', '', required_count[0]))
                    if len(hard_required_objectives) > required_objective_count:
                        self._simple_disable_regex(flagset, log, 'Changing required count', r'^Oreq:')
                        flagset.set(f'Oreq:{len(hard_required_objectives)}')
                        self._lib.push(log, ['correction', f'More hard required objectives set than number of objectives required, increasing required objective count to {len(hard_required_objectives)}.'])

            for gated in gated_objectives:
                gated_objective_index = int(self._lib.re_sub(r'^Ogated:', '', gated))
                bad_gated_conditions = False
                for hardreq in hard_required_objectives:
                    hard_required_index = int(self._lib.re_sub(r'^Ohardreq:', '', hardreq))
                    if hard_required_index == gated_objective_index:
                        bad_gated_conditions = True
                        self._lib.push(log, ['error', f'Cannot have objective #{hard_required_index} be both gated AND hard required.'])
                        break
                for doors_entrances in doors_entrances_rando:
                    bad_gated_conditions = True
                    self._lib.push(log, ['error', 'Doors and entrances rando does not currently support gated objectives.'])
                    break
                if bad_gated_conditions:
                    break

            win_flags = flagset.get_list(r'^Owin:')
          
            # Force Owin:crystal if classicforge, otherwise force Owin:game if no win result specified
            if flagset.has('Omode:classicforge') and not flagset.has('Owin:crystal'):
                flagset.set('Owin:crystal')
                self._lib.push(log, ['correction', 'Classic Forge is enabled; forced to add Owin:crystal'])
            elif len(win_flags) == 0:
                flagset.set('Owin:game')
                self._lib.push(log, ['correction', 'Objectives set without outcome specified; added Owin:game'])
                   
            # force Pkey if pass objective is set
            pass_quest_flags = flagset.get_list(r'^O\d+:quest_pass$')
            if len(pass_quest_flags) > 0 and flagset.has('Pnone'):
                flagset.set('Pkey')
                self._lib.push(log, ['correction', 'Pass objective is set without a pass flag; forced to add Pkey'])

            # for later, compute information about the potential objective-viable characters in the seed
            flags_objective_chars = []
            if flagset.has('Cvanilla'):
                if not (flagset.has('Cnofree') and not flagset.has('Ctreasure:free')):
                    for c in ['edward', 'tellah', 'palom', 'porom']:
                        self._lib.push(flags_objective_chars, c)
                if not (flagset.has('Cnoearned') and not flagset.has('Ctreasure:earned')):
                    for c in ['rydia', 'kain', 'rosa', 'yang', 'cid', 'edge', 'fusoya']:
                        self._lib.push(flags_objective_chars, c)
                flags_objective_chars_num = len(flags_objective_chars)
            else:
                only_flags = flagset.get_list(r'^Conly:')
                if len(only_flags) > 0:
                    for f in only_flags:
                        ch = self._lib.re_sub(r'^Conly:', '', f)
                        self._lib.push(flags_objective_chars, ch)
                else:
                    flags_objective_chars = ['cecil', 'kain', 'rydia', 'edward', 'tellah', 'rosa', 'yang', 'palom', 'porom', 'cid', 'edge', 'fusoya']
                    for f in flagset.get_list(r'^Cno:'):
                        ch = self._lib.re_sub(r'^Cno:', '', f)
                        self._lib.remove(flags_objective_chars, ch)
                flags_objective_chars_num = len(flags_objective_chars)
                distinct_flags = flagset.get_list(r'^Cdistinct:')
                if len(distinct_flags) > 0:
                    distinct_count = int(self._lib.re_sub(r'^Cdistinct:', '', distinct_flags[0]))
                    while flags_objective_chars_num > distinct_count:
                        flags_objective_chars_num -= 1

            # check for conflict between objective required characters and available ones
            char_objective_flags = flagset.get_list(r'^O\d+:char_')
            # for later, start building the list of mandatory character objectives
            character_pool = []
            required_chars = []
            if len(char_objective_flags) > 0:
                for f in char_objective_flags:
                    ch = self._lib.re_sub(r'^O\d+:char_', '', f)
                    self._lib.push(required_chars, ch)

                has_unavailable_characters = False
                for ch in required_chars:
                    if ch not in flags_objective_chars:
                        has_unavailable_characters = True

                if has_unavailable_characters:
                    if flagset.has('Cvanilla'):
                        self._lib.push(log, ['error', "Character objectives are set for characters that cannot be found in vanilla character assignment"])
                    else:
                        self._lib.push(log, ['error', "Character objectives are set for characters excluded from the randomization."])

                if flags_objective_chars_num < len(required_chars):
                    self._lib.push(log, ['error', "More character objectives are set than distinct characters allowed in the randomization."])

                if flagset.has('Cnofree') and flagset.has('Cnoearned') and not (flagset.has('Ctreasure:free') or flagset.has('Ctreasure:earned')):
                    self._lib.push(log, ['error', "Character objectives are set while no character slots will be filled"])         

                for ch in required_chars:
                    self._lib.push(character_pool, ch)                  
            
            for random_prefix in ['Orandom:', 'Orandom2:', 'Orandom3:']:    
                if len(flagset.get_list(f'^{random_prefix}' + r'(char|only)')) > 0 and flagset.has('Cnoearned') and flagset.has('Cnofree') and not flagset.has('Ctreasure:free') and not flagset.has('Ctreasure:earned'):
                    self._lib.push(log, ['error', f"Random character objectives specified in the {random_prefix} pool while no character slots will be filled."])
                    
            # remove random quest type specifiers if no random objectives specified
            for random_prefix in ['Orandom:', 'Orandom2:', 'Orandom3:']:
                if len(flagset.get_list(f'^{random_prefix}' + r'\d')) == 0:
                    self._simple_disable_regex(flagset, log, f'No random objectives specified for pool {random_prefix}', f'^{random_prefix}'+ r'[^\d]')

            # remove duplicate objectives relative to Omodes, since they take priority regardless (e.g. Omode:classicforge takes priority
            # over Od:quest_forge, in the sense that you will get no reward)
            if flagset.has('Omode:classicforge'):
                self._simple_disable_regex(flagset, log, 'Classic Forge takes priority over the normal Forge quest', r'^O[\d]:quest_forge')
            if flagset.has('Omode:classicgiant'):
                self._simple_disable_regex(flagset, log, 'Classic Giant takes priority over the normal Giant quest', r'^O[\d]:quest_giant')
            if flagset.has('Omode:fiends'):
                for b_fl in ['milon', 'kainazzo', 'valvalis', 'rubicant', 'elements']:
                    # milon will match milonz as well
                    self._simple_disable_regex(flagset, log, f'The specified boss is already an objective because of Omode:fiends', r'^O[\d]:boss_' + b_fl)

            total_mandatory_bosses = 0
            total_flexible_bosses = 0
            total_mandatory_tough_quests = 0
            total_flexible_tough_quests = 0
            total_mandatory_non_tough_quests = 0
            total_flexible_non_tough_quests = 0
            flexible_random_objective_count = 0
            total_objective_count = 0
            
            max_tough_quests = 22
            max_non_tough_quests = 17

            total_char_count = len(char_objective_flags)
            flexible_char_count = 0
            flexible_char_pool = []
            nonstarting_character_slots = 16
            if flagset.has('Cnofree') and not flagset.has('Ctreasure:free'):
                nonstarting_character_slots -= 5
            if flagset.has('Cnoearned') and not flagset.has('Ctreasure:earned'):
                nonstarting_character_slots -= 11
            elif flagset.has('Omode:classicgiant'):
                nonstarting_character_slots -= 1
            # cap the number of characters we can actually have objectives for by the number of slots there are available
            while flags_objective_chars_num > nonstarting_character_slots:
                flags_objective_chars_num -= 1

            specific_boss_objectives = []
            for fl in flagset.get_list(r'^O[\d]:boss_'):
                boss = self._lib.re_sub(r'^O\d+:boss_', '', fl)
                self._lib.push(specific_boss_objectives, boss)
            specific_tough_quest_objectives = []
            for fl in flagset.get_list(r'^O[\d]:quest_'):
                qu = self._lib.re_sub(r'^O\d+:', '', fl)
                self._lib.push(specific_tough_quest_objectives, qu)
            # check for the Pass objective for counting purposes before it gets removed; note that because the Pass objective forces
            # Pkey on if Pnone is there, we actually don't need the second part of the if condition
            if not flagset.has_any('Pkey', 'Pchests', 'Pshop') and not 'quest_pass' in specific_tough_quest_objectives:
                max_non_tough_quests -= 1
            for f in ['quest_mistcave', 'quest_waterfall', 'quest_antlionnest', 'quest_hobs', 'quest_fabul', 'quest_ordeals', 'quest_baroninn', 'quest_pass', 'quest_dwarfcastle', 'quest_lowerbabil', 'quest_unlocksewer', 'quest_music', 'quest_toroiatreasury', 'quest_magma', 'quest_unlocksealedcave', 'quest_bigwhale', 'quest_wakeyang']:
                if f in specific_tough_quest_objectives:
                    total_mandatory_non_tough_quests += 1
                self._lib.remove(specific_tough_quest_objectives, f) # already makes a check for inclusion
            all_specific_objectives = flagset.get_list(r'^O[\d]:')
            total_mandatory_bosses += len(specific_boss_objectives)
            total_mandatory_tough_quests += len(specific_tough_quest_objectives)
            total_objective_count += len(all_specific_objectives)
            if flagset.has('Omode:fiends'):
                total_mandatory_bosses += 6
                total_objective_count += 6
            if flagset.has('Omode:classicforge'):
                total_mandatory_tough_quests += 1
                total_objective_count += 1
            if flagset.has('Omode:classicgiant'):
                total_mandatory_tough_quests += 1
                total_objective_count += 1
            if len(flagset.get_list(r'^Omode:dkmatter')) > 0:
                total_objective_count += 1
            if len(flagset.get_list(r'^Omode:ki')) > 0:
                total_objective_count += 1
            if len(flagset.get_list(r'^Omode:goldhunter')) > 0:
                total_objective_count += 1
            if len(flagset.get_list(r'^Omode:bosscollector')) > 0:
                total_objective_count += 1
            if flagset.has('Omode:external'):
                total_objective_count += 1
            # special handling for the situation where the Pink Tail does not exist, to correctly count available tough quests
            # the Pink Tail is guaranteed unavailable on Kvanilla, or if there are 16 slots (Kstart:zonk) for 18 KI-type items (17+Pass)
            # the Pink Tail, without forcing, *might* be unavailable when there are N slots for N+1 KI-type items, since it'll randomly
            # choose between the Pink Tail and the Spoon for which item to place first; handle the forcing in objective_rando
            if flagset.has('Kvanilla'):
                if 'quest_tradepink' not in specific_tough_quest_objectives:
                    max_tough_quests -= 1
                else: 
                    self._lib.push(log, ['error', "The objective-required Pink Tail is not available with vanilla key item placement"])
            elif not flagset.has_any('Ksummon', 'Kmoon', 'Kforge', 'Kpink',
                           'Kmiab:standard', 'Kmiab:above', 'Kmiab:below', 'Kmiab:lst',
                           'Kmiab:all') and flagset.has('Pkey') and not flagset.has('Owin:crystal') and flagset.has('Kstart:zonk'):
                if 'quest_tradepink' not in specific_tough_quest_objectives:
                    max_tough_quests -= 1
                else:
                    self._lib.push(log, ['error', "Both non-essential key items are removed on these flags, so the objective-required Pink Tail is not available"])

            if flagset.has('Bvanilla'):
                for fl in specific_boss_objectives:
                    current_boss = self._lib.re_sub(r'^O\d+:boss_', '', fl)
                    if current_boss == 'waterhag':
                        self._lib.push(log, ['error', f"Objective boss specified ({current_boss}) when that boss is not in the vanilla boss assignment"])
                    elif ((current_boss == 'kingqueen' and flagset.has('Bremove:kingqueen_slot'))
                            or (current_boss == 'officer' and flagset.has('Bremove:officer_slot'))):
                        self._lib.push(log, ['error', f"Objective specified for a boss removed from the vanilla boss assignment by Bremove: ({current_boss})"])

            # for the purposes of making it easier for fix() to find ways to make the objectives work,
            # reorder the three objective groups by how restrictive they are in terms of objectives.
            # assign each a score, and then "sort" (if/elif/else)
            # 1. char only, count only[] or just # available chars, whichever is smaller if only[] > 0
            # 2. tough_quest only, 22
            # 3. tough_quest and char, 22 + num chars ^^
            # 4. quest, 22+17 = 39 + 20 for separation
            # 5. quest and char, 39 + num chars + 20
            # 6. bosses? +100, keep the same order because it doesn't matter at all
            # 7. no one cares if it's an empty group
            # more objectives should be a tiebreaker, so I guess add num objectives - 4 (to go from -3 to +4).

            # in addition, here is where we do a cursory "remove characters" pass to tidy up the flags

            group_scores = []
            for rand_pref in ['Orandom:', 'Orandom2:', 'Orandom3:']:
                rand_only_char_flags = flagset.get_list(f'{rand_pref}only')
                # strip flagset of only[char] flags if those characters cannot be in the seed based on flags_objective_chars above
                if len(rand_only_char_flags) > 0:
                    for fl in rand_only_char_flags:
                        ch = self._lib.re_sub(f'{rand_pref}only', '', fl)
                        if ch not in flags_objective_chars:
                            flagset.unset(fl)
                            self._lib.push(log, ['correction', f'Random character objective restrictions set for characters guaranteed not to appear in the seed; removing {fl}'])
                        # ... and if those characters already have custom objectives set for them
                        elif ch in required_chars:
                            flagset.unset(fl)
                            self._lib.push(log, ['correction', f'Random character objective restrictions set for characters with custom objectives set; removing {fl}'])

                # correct only[char] without char
                if not flagset.has(f'{rand_pref}char') and len(rand_only_char_flags) > 0:
                    flagset.set(f'{rand_pref}char')
                    self._lib.push(log, ['correction', f'Random objectives requiring specific characters set without Orandom:char; setting {rand_pref}char'])

                all_customized_rand_flags = flagset.get_list(f'^{rand_pref}'+ r'[^\d]')
                num_rand_objectives = flagset.get_list(f'^{rand_pref}'+ r'[\d]')
                if len(num_rand_objectives) == 0:
                    self._lib.push(group_scores, 0)
                    continue
                grp_obj_num = int(self._lib.re_sub(f'^{rand_pref}', '', num_rand_objectives[0]))

                # strip out only[char] flags to get only: boss, quest or tough_quest, char
                rand_category_flags = []
                for fl in all_customized_rand_flags:
                    if fl not in rand_only_char_flags:
                        self._lib.push(rand_category_flags, fl)

                if len(rand_category_flags) == 0 or f'{rand_pref}boss' in rand_category_flags:
                    self._lib.push(group_scores, 100)
                    continue

                # only len == 1 or 2 cases left, so just check and add
                grp_sc = 0
                if f'{rand_pref}char' in rand_category_flags:
                    if len(rand_only_char_flags) > 0 and len(rand_only_char_flags) < flags_objective_chars_num:
                        grp_sc += len(rand_only_char_flags)
                    else:
                        grp_sc += flags_objective_chars_num
                if f'{rand_pref}tough_quest' in rand_category_flags:
                    grp_sc += max_tough_quests
                elif f'{rand_pref}quest' in rand_category_flags:
                    grp_sc += max_tough_quests + max_non_tough_quests + 20

                grp_sc += (grp_obj_num - 4)
                self._lib.push(group_scores, grp_sc)

            # sort the groups by score (lower score -> harder to place -> do first)
            if group_scores[0] <= group_scores[1]:
                if group_scores[2] < group_scores[0]:
                    sorted_groups = ['Orandom3:', 'Orandom:', 'Orandom2:']
                elif group_scores[2] >= group_scores[1]:
                    sorted_groups = ['Orandom:', 'Orandom2:', 'Orandom3:']
                else:
                    sorted_groups = ['Orandom:', 'Orandom3:', 'Orandom2:']
            else:
                if group_scores[2] < group_scores[1]:
                    sorted_groups = ['Orandom3:', 'Orandom2:', 'Orandom:']
                elif group_scores[2] >= group_scores[0]:
                    sorted_groups = ['Orandom2:', 'Orandom:', 'Orandom3:']
                else:
                    sorted_groups = ['Orandom2:', 'Orandom3:', 'Orandom:']

            for random_prefix in sorted_groups:
                if len(flagset.get_list(f'^{random_prefix}')) == 0:
                    continue

                random_only_char_flags = flagset.get_list(f'{random_prefix}only')

                # skip if no number of objectives has been set
                all_customized_random_flags = flagset.get_list(f'^{random_prefix}'+ r'[^\d]')
                num_random_objectives = flagset.get_list(f'^{random_prefix}'+ r'[\d]')
                if len(num_random_objectives) == 0:
                    continue
                group_obj_num = int(self._lib.re_sub(f'^{random_prefix}', '', num_random_objectives[0]))
                total_objective_count += group_obj_num

                # strip out only[char] flags to get only: boss, quest or tough_quest, char
                random_category_flags = []
                for fl in all_customized_random_flags:
                    if fl not in random_only_char_flags:
                        self._lib.push(random_category_flags, fl)

                # if bosses are available, they allow all other objective types to be skipped because there are >=32 of them
                # (if we run into issues with too many boss objectives, then we've already hit the objective cap)
                # note: this logic does not survive into 5.0, but that's already got a different objective group system
                bosses_available = False
                if f'{random_prefix}boss' in random_category_flags or len(random_category_flags) == 0:
                    bosses_available = True

                # identify how many character objectives are *actually* available for this group, based on only[char] flags
                # and the characters available/seen so far
                only_chars_list = []
                for fl in random_only_char_flags:
                    self._lib.push(only_chars_list, fl[len(f'{random_prefix}only'):])
                just_in_case_mandatory_char_pool = []

                # identify if there are only character objectives or not
                only_char_objectives = False
                if f'{random_prefix}char' in random_category_flags and len(random_category_flags) == 1:
                    only_char_objectives = True
 
                # the next section only matters if we even have character objectives: otherwise, default
                # to no available character objectives (which makes sense)
                theoretical_available_characters = 0
                actual_available_characters = 0
                duplicate_char_count = 0 # len(character_pool)
                if f'{random_prefix}char' in random_category_flags:
                    if len(random_only_char_flags) > 0 and len(random_only_char_flags) < group_obj_num and only_char_objectives == True:
                        self._lib.push(log, ['error', f'Random objectives requiring fewer specific characters ({len(random_only_char_flags)}) than number of objectives ({group_obj_num})'])
                        break
                    elif flags_objective_chars_num < group_obj_num and only_char_objectives == True:
                        self._lib.push(log, ['error', f'Fewer characters available ({flags_objective_chars_num}) than required number of random character objectives ({group_obj_num})'])
                        break
                    else:
                        if len(random_only_char_flags) > 0:
                            # at this point, the character *can* be in the game (is in flags_objective_chars)
                            ch_list = only_chars_list
                            ch_count_cap = len(random_only_char_flags)
                        else:
                            # start with the number of possible character objectives in the seed (possibly smaller than the number
                            # of characters that are available, due to slot restrictions/character uncertainty)
                            ch_list = flags_objective_chars
                            ch_count_cap = flags_objective_chars_num
                        for current_char in ch_list:
                            # at this point, the character *can* be in the game (is in flags_objective_chars)
                            theoretical_available_characters += 1
                            # is this character already a mandatory char objective? 
                            if current_char in character_pool:
                                duplicate_char_count += 1
                            else:
                                # if this is a guaranteed character objective, and it *must* be chosen, push to character_pool
                                if only_char_objectives and ch_count_cap == group_obj_num:
                                    self._lib.push(character_pool, current_char)
                                    self._lib.remove(flexible_char_pool, current_char) # built-in check for inclusion
                                else:
                                    self._lib.push(just_in_case_mandatory_char_pool, current_char)
                                    if current_char not in flexible_char_pool:
                                        self._lib.push(flexible_char_pool, current_char)                        

                    # ensure that we can't actually have try to assign too many character objectives
                    if theoretical_available_characters > flags_objective_chars_num:
                        theoretical_available_characters = flags_objective_chars_num
                    # and ensure that we're counting the real number of character objectives that we've already assigned,
                    # given by total_char_count: if total_char_count > duplicate_char_count, then increase duplicate_char_count,
                    # but only if we weren't restricting characters to only specific ones
                    if total_char_count > duplicate_char_count and len(random_only_char_flags) == 0:
                        duplicate_char_count = total_char_count
                    # theoretical_available_characters - duplicate_char_count is the number of new potential char objectives that
                    # this group can assign that we haven't already guaranteed
                    actual_available_characters = theoretical_available_characters - duplicate_char_count

                    # actual_available_characters is the true maximum number of character objectives that this objective group can pick,
                    # so if we're short on characters and we *must* pick characters, then throw an error
                    if actual_available_characters < group_obj_num and only_char_objectives == True:
                        self._lib.push(log, ['error', f'Not enough unique characters for pool {random_prefix}. Other pools and custom objectives have consumed too many characters by now'])
                        break

                # if we're here, then either it's not only character objectives, or there are 
                # at least as many actual_available_characters as group_obj_num.
                # in the former case, it's possible that we have a minimum number of required non-charater objectives,
                # which is hyper relevant if we don't have bosses. If we didn't have character objectives to begin with,
                # min_non_char_objectives will always be group_obj_num
                min_non_char_objectives = 0
                if actual_available_characters < group_obj_num:
                    min_non_char_objectives = group_obj_num - actual_available_characters
                max_char_objectives = actual_available_characters
                # in addition, there may be all characters available, but of course we can only pick out so many objectives total
                while max_char_objectives > group_obj_num:
                    max_char_objectives -= 1

                # now we start adding to our objective counts.
                # key thing to keep in mind: if we have mandatory objective types and we run out of room (which would otherwise
                # throw an error), we can use some of the flexible objectives to compensate (until we use them up)
                if bosses_available:
                    # when bosses are available, everything is flexible (unless we're hitting the 32 objective cap,
                    # which takes priority)
                    if len(random_category_flags) == 1:
                        # in this case, there are only boss objectives
                        total_mandatory_bosses += group_obj_num
                    elif len(random_category_flags) == 2 and f'{random_prefix}char' in random_category_flags:
                        # here, we have bosses and characters only, so some bosses may be required
                        total_mandatory_bosses += min_non_char_objectives
                        total_flexible_bosses += group_obj_num - min_non_char_objectives
                        flexible_char_count += max_char_objectives
                        flexible_random_objective_count += group_obj_num - min_non_char_objectives
                    elif len(random_category_flags) == 2 and f'{random_prefix}char' not in random_category_flags:
                        # here we have bosses and either quests or tough quests
                        if f'{random_prefix}quest' in random_category_flags:
                            # here we need to ensure that our flexible counts are not exceeding the max
                            # allowed counts for these objectives: 22 for tough quests, 17 for non-tough quests
                            non_tough_quest_room = max_non_tough_quests - total_mandatory_non_tough_quests - total_flexible_non_tough_quests
                            tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                            # we have four cases (and one subcase), depending on how many quests/tough quests we can have
                            if non_tough_quest_room < group_obj_num and tough_quest_room >= group_obj_num:
                                total_flexible_non_tough_quests += non_tough_quest_room
                                total_flexible_tough_quests += group_obj_num
                                total_flexible_bosses += group_obj_num
                                flexible_random_objective_count += group_obj_num
                            elif non_tough_quest_room >= group_obj_num and tough_quest_room < group_obj_num:
                                total_flexible_non_tough_quests += group_obj_num
                                total_flexible_tough_quests += tough_quest_room
                                total_flexible_bosses += group_obj_num
                                flexible_random_objective_count += group_obj_num
                            elif non_tough_quest_room < group_obj_num and tough_quest_room < group_obj_num:
                                total_flexible_non_tough_quests += non_tough_quest_room
                                total_flexible_tough_quests += tough_quest_room
                                if non_tough_quest_room + tough_quest_room < group_obj_num:
                                    total_mandatory_bosses += group_obj_num - non_tough_quest_room - tough_quest_room
                                    total_flexible_bosses += non_tough_quest_room + tough_quest_room
                                    flexible_random_objective_count += non_tough_quest_room + tough_quest_room
                                else:
                                    total_flexible_bosses += group_obj_num
                                    flexible_random_objective_count += group_obj_num
                            else:
                                total_flexible_non_tough_quests += group_obj_num
                                total_flexible_tough_quests += group_obj_num
                                total_flexible_bosses += group_obj_num
                                flexible_random_objective_count += group_obj_num
                        elif f'{random_prefix}tough_quest' in random_category_flags:
                            # same, but only for tough_quests, which decreases the number of cases
                            tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                            if tough_quest_room < group_obj_num:
                                total_flexible_tough_quests += tough_quest_room
                                total_mandatory_bosses += group_obj_num - tough_quest_room
                                total_flexible_bosses += tough_quest_room
                                flexible_random_objective_count += tough_quest_room
                            else:
                                total_flexible_tough_quests += group_obj_num
                                total_flexible_bosses += group_obj_num
                                flexible_random_objective_count += group_obj_num
                    elif len(random_category_flags) == 3 and f'{random_prefix}tough_quest' in random_category_flags:
                        # here, we have all possible objectives available except non-tough quests
                        tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                        # so, we have three cases
                        if tough_quest_room < group_obj_num and min_non_char_objectives == 0:
                            total_flexible_tough_quests += tough_quest_room
                            flexible_char_count += max_char_objectives # which in this case is group_obj_num
                            total_flexible_bosses += group_obj_num
                            flexible_random_objective_count += group_obj_num
                        elif tough_quest_room < group_obj_num and min_non_char_objectives > 0:
                            # possibly have mandatory bosses here
                            total_flexible_tough_quests += tough_quest_room
                            flexible_char_count += max_char_objectives
                            if tough_quest_room + max_char_objectives < group_obj_num:
                                total_mandatory_bosses += group_obj_num - tough_quest_room - max_char_objectives
                                total_flexible_bosses += tough_quest_room + max_char_objectives
                                flexible_random_objective_count += tough_quest_room + max_char_objectives
                            else:
                                total_flexible_bosses += group_obj_num
                                flexible_random_objective_count += group_obj_num
                        else: 
                            # tough_quest_room >= group_obj_num means we don't care what min_non_char_objectives does
                            flexible_char_count += max_char_objectives
                            total_flexible_tough_quests += group_obj_num
                            total_flexible_bosses += group_obj_num
                            flexible_random_objective_count += group_obj_num
                    else:
                        # all types of objectives are available
                        non_tough_quest_room = max_non_tough_quests - total_mandatory_non_tough_quests - total_flexible_non_tough_quests
                        tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                        if non_tough_quest_room < group_obj_num:
                            total_flexible_non_tough_quests += non_tough_quest_room
                        else:
                            total_flexible_non_tough_quests += group_obj_num
                        if tough_quest_room < group_obj_num:
                            total_flexible_non_tough_quests += tough_quest_room
                        else:
                            total_flexible_tough_quests += group_obj_num
                        flexible_char_count += max_char_objectives
                        total_flexible_bosses += group_obj_num
                        flexible_random_objective_count += group_obj_num

                # now bosses are *not* available, which means we either have just characters, just quests/tough quests,
                # or both of those categories.
                elif len(random_category_flags) == 1:
                    if f'{random_prefix}char' in random_category_flags:
                        # only characters! so we have mandatory character objectives, and we've already
                        # confirmed that we have enough characters available for them, and handled with
                        # mandatory/flexible character pool stuff
                        total_char_count += group_obj_num
                    elif f'{random_prefix}quest' in random_category_flags:
                        # quests and tough quests, do similar to the above
                        non_tough_quest_room = max_non_tough_quests - total_mandatory_non_tough_quests - total_flexible_non_tough_quests
                        tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                        if non_tough_quest_room + tough_quest_room < group_obj_num:
                            # I think this situation is impossible without hitting the 32 objective cap, but good to have it anyway
                            # and we'll ignore the additional subcase of also needing flexible quests, since that's blowing past 32 objectives
                            self._lib.push(log, ['error', f'Too many quests (tough and non-tough) have been consumed by now ({random_prefix}), between custom objectives and other pools'])
                            break
                        # now, we carefully add to totals
                        if non_tough_quest_room < group_obj_num and tough_quest_room >= group_obj_num:
                            total_flexible_non_tough_quests += non_tough_quest_room
                            total_mandatory_tough_quests += group_obj_num - non_tough_quest_room
                            total_flexible_tough_quests += non_tough_quest_room
                            flexible_random_objective_count += non_tough_quest_room
                        elif non_tough_quest_room >= group_obj_num and tough_quest_room < group_obj_num:
                            total_flexible_tough_quests += tough_quest_room
                            total_mandatory_non_tough_quests += group_obj_num - tough_quest_room
                            total_flexible_non_tough_quests += tough_quest_room
                            flexible_random_objective_count += tough_quest_room
                        elif non_tough_quest_room < group_obj_num and tough_quest_room < group_obj_num:
                            total_mandatory_non_tough_quests += group_obj_num - tough_quest_room
                            total_flexible_non_tough_quests += non_tough_quest_room - (group_obj_num - tough_quest_room)
                            total_mandatory_tough_quests += group_obj_num - non_tough_quest_room
                            total_flexible_tough_quests += tough_quest_room - (group_obj_num - non_tough_quest_room)
                            flexible_random_objective_count += non_tough_quest_room + tough_quest_room - group_obj_num
                        else:
                            total_flexible_non_tough_quests += group_obj_num
                            total_flexible_tough_quests += group_obj_num
                            flexible_random_objective_count += group_obj_num
                    else:
                        # just tough quests! that's the only case left
                        tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                        if tough_quest_room < group_obj_num:
                            # check if we can use flexible tough quests to hit the required number
                            if tough_quest_room + total_flexible_tough_quests < group_obj_num:
                                self._lib.push(log, ['error', f'Too many tough quests have been consumed by now ({random_prefix}), between custom objectives and other pools'])
                                break
                            else:
                                # use flexibility here
                                total_mandatory_tough_quests += tough_quest_room
                                total_flexible_tough_quests -= (group_obj_num - tough_quest_room)
                        else:
                            total_mandatory_tough_quests += group_obj_num
                
                else:
                    # we have characters and either all quests or just tough quests.
                    if f'{random_prefix}tough_quest' in random_category_flags:
                        tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                        if tough_quest_room + max_char_objectives < group_obj_num:
                            # check if flexible tough quests are enough
                            if tough_quest_room + max_char_objectives + total_flexible_tough_quests < group_obj_num:
                                self._lib.push(log, ['error', f'Too many tough quests and characters have been consumed by now ({random_prefix}), between custom objectives and other pools'])
                                break
                            else:
                                # the way out is to use flexible tough quests
                                total_mandatory_tough_quests += tough_quest_room
                                total_flexible_tough_quests -= (group_obj_num - tough_quest_room - max_char_objectives)
                                total_char_count += max_char_objectives
                        elif tough_quest_room < min_non_char_objectives:
                            # ... I think it's actually the case that this case is equivalent, at this point, 
                            # to the previous one, but it's good to be sure.
                            if tough_quest_room + total_flexible_tough_quests < min_non_char_objectives:
                                self._lib.push(log, ['error', f'Too many tough quest objectives are required for the number of character objectives that are left ({random_prefix})'])
                                break
                            else:
                                # the way out is to use flexible tough quests; yes, these numbers add up here
                                total_mandatory_tough_quests += tough_quest_room
                                total_flexible_tough_quests -= (min_non_char_objectives - tough_quest_room)
                                total_char_count += max_char_objectives
                        elif min_non_char_objectives == 0:
                            # we can fill the entire group with character objectives!
                            # but we might have *guaranteed* char objectives
                            if tough_quest_room < group_obj_num:
                                total_char_count += group_obj_num - tough_quest_room
                                flexible_char_count += tough_quest_room
                                total_flexible_tough_quests += tough_quest_room
                                # if tough_quest_room was actually just 0, then these are *mandatory* character objectives,
                                # so if actual_available_characters is equal to group_obj_num, then we need to
                                # push all of the characters to character_pool (possibly removing from flexible_char_pool)
                                if actual_available_characters == group_obj_num:
                                    for ch in just_in_case_mandatory_char_pool:
                                        self._lib.push(character_pool, ch)
                                        self._lib.remove(flexible_char_pool, ch) # built-in check for inclusion
                                else:
                                    flexible_random_objective_count += tough_quest_room
                            else:
                                flexible_char_count += group_obj_num
                                total_flexible_tough_quests += group_obj_num
                                flexible_random_objective_count += group_obj_num
                        else:
                            # we *must* have non-character objectives.
                            if tough_quest_room < group_obj_num:
                                # keeping flexibility in tough quests in mind, we might not have character objectives at all
                                if tough_quest_room + total_flexible_tough_quests < group_obj_num:
                                    # we also *must* have some character objectives
                                    total_char_count += group_obj_num - (tough_quest_room + total_flexible_tough_quests)
                                    flexible_char_count += max_char_objectives - (group_obj_num - tough_quest_room - total_flexible_tough_quests)
                                    total_mandatory_tough_quests += min_non_char_objectives
                                    # before we change total_flexible_tough_quests, we need to up the flexible random objective count;
                                    # the amount we add is just group_obj_num minus the amounts we added to total_char_count and total_mandatory_tough_quests
                                    flexible_random_objective_count += tough_quest_room + total_flexible_tough_quests - min_non_char_objectives
                                    total_flexible_tough_quests += tough_quest_room - min_non_char_objectives
                                else:
                                    # we can use flexible tough quests to handle everything
                                    if tough_quest_room < min_non_char_objectives:
                                        total_mandatory_tough_quests += tough_quest_room
                                        total_flexible_tough_quests += (group_obj_num - min_non_char_objectives) - (min_non_char_objectives - tough_quest_room)
                                        flexible_char_count += max_char_objectives
                                        flexible_random_objective_count += group_obj_num - min_non_char_objectives
                                    else:
                                        total_mandatory_tough_quests += min_non_char_objectives
                                        total_flexible_tough_quests += group_obj_num - min_non_char_objectives
                                        flexible_char_count += max_char_objectives
                                        flexible_random_objective_count += group_obj_num - min_non_char_objectives
                            else:
                                # some mandatory tough_quests, and the rest are flexible
                                total_mandatory_tough_quests += min_non_char_objectives
                                total_flexible_tough_quests += group_obj_num - min_non_char_objectives
                                flexible_char_count += max_char_objectives
                                flexible_random_objective_count += group_obj_num - min_non_char_objectives
                    
                    else:
                        # chars, non-tough quests, and tough quests are what's left. This should never
                        # pose issues, given how many non-tough quests there are. In particular, 
                        # even in the last group, you can only have 2+8+8+8 = 26 quest/tough quests used up, and 39-26 = 13 > 8,
                        # so non_tough_quest_room + tough_quest_room will always be larger than group_obj_num here.
                        non_tough_quest_room = max_non_tough_quests - total_mandatory_non_tough_quests - total_flexible_non_tough_quests
                        tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                        if min_non_char_objectives == 0:
                            # can fill with char objectives; we'll never *need* char objectives, but
                            # there might be caps on non/tough quests
                            flexible_char_count += group_obj_num
                            flexible_random_objective_count += group_obj_num
                            if non_tough_quest_room < group_obj_num:
                                total_flexible_non_tough_quests += non_tough_quest_room
                            else:  
                                total_flexible_non_tough_quests += group_obj_num
                            if tough_quest_room < group_obj_num:
                                total_flexible_tough_quests += tough_quest_room
                            else:
                                total_flexible_tough_quests += group_obj_num
                        else:
                            # there are guaranteed non-char objectives.
                            # which mostly just means that we cap the char objective addition,
                            # and exactly one of tough/non-tough quests because of the above calculation
                            flexible_char_count += group_obj_num - min_non_char_objectives
                            flexible_random_objective_count += group_obj_num
                            if non_tough_quest_room < group_obj_num:
                                total_flexible_non_tough_quests += non_tough_quest_room
                                total_flexible_tough_quests += group_obj_num
                            elif tough_quest_room < group_obj_num:
                                total_flexible_non_tough_quests += group_obj_num
                                total_flexible_tough_quests += tough_quest_room
                            else:
                                # can fill the group with either non/tough quests
                                total_flexible_non_tough_quests += group_obj_num
                                total_flexible_tough_quests += group_obj_num

                # we have now, finally, hopefully, added to all of the relevant counts as required
                # by the flags and what we've seen previously

            # mostly future-proofing, because in this situation we'd hit the max objective limit first.
            max_bosses = 34
            boss_slots_removed = 0
            removed_bosses_flags = flagset.get_list(rf'^Bremove:')
            for slot in removed_bosses_flags:
                max_bosses -= 1
                boss_slots_removed += 1
            if total_mandatory_bosses > max_bosses:
                self._lib.push(log, ['error', f"{total_mandatory_bosses} guaranteed boss objectives specified with only {max_bosses} bosses available ({boss_slots_removed} bosses removed)"])

            if total_mandatory_tough_quests > max_tough_quests:
                self._lib.push(log, ['error', f"{total_mandatory_tough_quests} guaranteed tough quest objectives specified with only {max_tough_quests} tough quests available"])
            # no need to check this for non-tough quests, of course

            if total_objective_count > 32:
                self._lib.push(log, ['error', "More than 32 objectives specified"])                           
            #print(f'Total potential bosses is {total_potential_bosses} Objectives is {total_objective_count}')            

            # ensure that there are actually enough character slots being filled to satisfy the objective requirements
            if total_char_count > nonstarting_character_slots:
                self._lib.push(log, ['error', f'Not enough available non-starting character slots for all of the mandatory character objectives specified (between fixed objectives and random pools). Either add more character slots back in, remove character objectives, or allow other objective types for some random pools.'])
            elif flagset.has('Cvanilla'):
                # on Cvanilla, we know exactly which characters are in the seed, so we need to cap the number of character objectives
                # at how many distinct characters there are.
                available_vanilla_chars = 11
                if (flagset.has('Cnofree') and not flagset.has('Ctreasure:free')):
                    available_vanilla_chars -= 4
                if (flagset.has('Cnoearned') and not flagset.has('Ctreasure:earned')):
                    available_vanilla_chars -= 7
                if total_char_count > available_vanilla_chars:
                    self._lib.push(log, ['error', f'Not enough available non-starting vanilla characters for all of the mandatory character objectives specified (between fixed objectives and random pools). Either add more character slots back in, remove character objectives, or allow other objective types for some random pools.'])
            else: 
                distinct_flags = flagset.get_list(r'^Cdistinct:')
                if len(distinct_flags) > 0:
                    # we've already ensured that *specified* objective characters are available, but we need to ensure that the random objectives
                    # don't insist on too many other characters
                    distinct_count =  int(self._lib.re_sub(r'^Cdistinct:', '', distinct_flags[0]))
                    if total_char_count > distinct_count:
                        self._lib.push(log, ['error', f'Too few distinct characters specified for the mandatory character objectives. Either increase the number of distinct characters, or remove character objectives.'])
            
            # ... it's likely that due to the refactor above, the next part is useless. 
            # we have a maximum number of "flexible" tough quests. but, there are only 22 of those, some of which are taken up by mandatory tough quests.
            # so, decrease total_flexible_tough_quests until we find how many we can actually use.
            while total_mandatory_tough_quests + total_flexible_tough_quests > max_tough_quests:
                total_flexible_tough_quests -= 1
                # when it hits zero, we already know there aren't too many mandatory tough quests, so this while loop ends
            # same thing for non_tough quests: there are 17 of those.
            while total_mandatory_non_tough_quests + total_flexible_non_tough_quests > max_non_tough_quests:
                total_flexible_non_tough_quests -= 1
                # here, total_mandatory_non_tough_quests is at most 8.
            # same thing for bosses: there are max_bosses of those.
            while total_mandatory_bosses + total_flexible_bosses > max_bosses:
                total_flexible_bosses -= 1
                # it is almost certain that we don't subtract off anything here, but might as well future-proof it
            
            # finally, check if the number of flexible objectives is sufficient
            if flexible_char_count + total_flexible_bosses + total_flexible_non_tough_quests + total_flexible_tough_quests < flexible_random_objective_count:
                self._lib.push(log, ['error', f'There are too many restrictions on the types of random objectives to select enough random objectives satisfying the flags.'])

        challenges = flagset.get_list(r'^-wacky:')
        if challenges:
            # Simplified wacky compatibility logic
            # If one of these is set, none of the others in this group can be
            WACKY_SET_1 = ['afflicted', 'menarepigs', 'mirrormirror', 'skywarriors', 'zombies']
            # If one of the above is set, none of these can be
            WACKY_SET_2 = ['battlescars', 'payablegolbez', 'tellahmaneuver', 'worthfighting']
            # These are sets of mutually incompatible modes
            WACKY_SET_3 = [
                ['3point', 'afflicted', 'battlescars', 'menarepigs', 'mirrormirror', 'skywarriors', 'unstackable', 'zombies'],
                ['afflicted', 'friendlyfire'],
                ['battlescars', 'afflicted', 'zombies', 'worthfighting'],
                ['darts', 'musical', 'skillissue'],
                ['3point', 'tellahmaneuver'],
            ]

            for c in challenges:
                mode = self._lib.re_sub(r'-wacky:', '', c)
                if mode in WACKY_SET_1:
                    self._simple_disable(flagset, log, 'Can only have one enforced status wacky mode', [fr'-wacky:{m}' for m in WACKY_SET_1 if m != mode])
                    self._simple_disable(flagset, log, 'Modes are incompatible with enforced status wacky modes', [fr'-wacky:{m}' for m in WACKY_SET_2])
                for group in WACKY_SET_3:
                    if mode in group:
                        self._simple_disable(flagset, log, f'Wacky modes are incompatible with {mode}', [fr'-wacky:{m}' for m in group if m != mode])
                    
        
        return log


