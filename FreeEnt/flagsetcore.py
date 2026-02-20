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
        if flagset.has('Kunsafer') and not flagset.has_any('Kmoon', 'Kmiab:lst', 'Kmiab:all'):
            flagset.set('Kmoon')
            self._lib.push(log, ['correction', 'Kunsafer requires placing key items on the moon; adding Kmoon'])

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

        if flagset.has('Chero'):
            self._simple_disable_regex(flagset, log, 'Hero challenge includes smith weapon', r'^-smith:(super|alt|playable)')

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
            self._simple_disable(flagset, log, 'Bosses not randomized', ['Bunsafe'])
            self._simple_disable_regex(flagset, log, 'Bosses not randomized', r'^Brestrict:')

        if flagset.has('Evanilla'):
            self._simple_disable(flagset, log, 'Encounters are vanilla', ['Ekeep:behemoths', 'Ekeep:doors', 'Edanger'])

        if len(flagset.get_list(r'^-smith:playable')) == len(flagset.get_list(r'^-smith:')):
            self._simple_disable(flagset, log, 'No smith item requested', ['-smith:playable'])
        if flagset.has('-smith:omni') and not (flagset.has_any('-smith:super', 'Chero')):
            self._simple_disable(flagset, log, 'No FF4A weapon available', ['-smith:omni'])

        # add restrictions in case people try to fudge the fusoya flags
        if flagset.has('-fusoya:slowstart') and flagset.has('-fusoya:uncapped'):
            self._simple_disable(flagset, log, 'Uncapped FuSoYa cannot also have slowstart', ['-fusoya:slowstart'])
        if flagset.has('-fusoya:location') and flagset.has('-fusoya:slowstart'):
            self._simple_disable(flagset, log, 'Location FuSoYa cannot have slowstart', ['-fusoya:slowstart'])
        if flagset.has('-fusoya:nerfed'):
            self._simple_disable_regex(flagset, log, 'Nerfed FuSoYa cannot have slowstart or unlearn spells', r'^-fusoya:(slowstart|unlearn)')
        if flagset.has('-fusoya:vanilla'):
            self._simple_disable_regex(flagset, log, 'Vanilla FuSoYa cannot have his HP or spells change', r'^-fusoya:(slowstart|unlearn|randomhp)')

        if flagset.has('-monsterflee') and not flagset.has('-monsterevade'):
            flagset.set('-monsterevade')
            self._lib.push(log, ['correction', 'Monsters require evade to flee; forced to add -monsterevade'])

        if flagset.has_any('-entrancesrando:normal','-entrancesrando:gated','-entrancesrando:blueplanet','-entrancesrando:why','-entrancesrando:all'):
            self._simple_disable_regex(flagset, log, 'Entrances rando takes priority', r'^-doorsrando')

        if not flagset.has_any('-entrancesrando:normal','-entrancesrando:gated','-entrancesrando:blueplanet',
                               '-entrancesrando:why','-entrancesrando:all','-doorsrando:normal','-doorsrando:gated',
                               '-doorsrando:blueplanet','-doorsrando:why','-doorsrando:all'):
            self._simple_disable(flagset, log, 'Removing doors rando related flags when no doors/entrances option is enabled ', ['-calmness','-forcesealed'])



        if flagset.has_any('-entrancesrando:normal','-entrancesrando:gated','-entrancesrando:blueplanet','-entrancesrando:why','-entrancesrando:all'):
            self._simple_disable_regex(flagset, log, 'Entrances rando takes priority', r'^-doorsrando')

        if not flagset.has_any('-entrancesrando:normal','-entrancesrando:gated','-entrancesrando:blueplanet',
                               '-entrancesrando:why','-entrancesrando:all','-doorsrando:normal','-doorsrando:gated',
                               '-doorsrando:blueplanet','-doorsrando:why','-doorsrando:all'):
            self._simple_disable(flagset, log, 'Removing doors rando related flags when no doors/entrances option is enabled ', ['-calmness','-forcesealed'])

        # temporarily prevent usage of -starting:underground and -starting:blackchocobo, until Doors are fixed
        if flagset.has_any('-starting:underground','-starting:blackchocobo'):
            self._lib.push(log, ['error', "Different starting location flags are not currently available; remove them and try again."])

        if flagset.has('-z:physical') and flagset.has('-z:whichbang'):
            self._simple_disable(flagset, log, 'No guaranteed Big Bangs in script', ['-z:whichbang'])

        if flagset.has_any('-z:chaos', '-z:lavosshell') and flagset.has('-z:phaseshift'):
            self._simple_disable(flagset, log, 'Random phases take precedence over shuffled phases', ['-z:phaseshift'])

        # add in a couple other restrictions about Z fight stuff

        all_spoiler_flags = flagset.get_list(r'^-spoil:')
        sparse_spoiler_flags = flagset.get_list(r'^-spoil:sparse')
        if (len(all_spoiler_flags) > 0 and len(all_spoiler_flags) == len(sparse_spoiler_flags)):
            self._simple_disable_regex(flagset, log, 'No spoilers requested', r'^-spoil:sparse')

        if flagset.has('Chi') and flagset.has('Chero') and flagset.has('Cparty:1'):  
            self._simple_disable(flagset, log, 'No room for characters to be added with Chero and Max Party size of 1', ['Chi'])

        if flagset.has('Cfifo') and flagset.has('Chero') and flagset.has('Cparty:1'):  
            self._simple_disable(flagset, log, 'Cant remove characters with Chero and Max Party size of 1', ['Cfifo'])

        if flagset.has('Cpermajoin') and flagset.has('Cfifo'):
            self._simple_disable(flagset, log, 'Permajoin and Remove Oldest are incompatible', ['Cfifo'])


        # Objectives logic
        if flagset.has('Onone'):
            self._simple_disable_regex(flagset, log, 'No objectives set', r'^O(win|req):')
            self._simple_disable_regex(flagset, log, 'No objectives set', r'^-exp:objectivebonus')
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

            gated_objectives = flagset.get_list(r'^Ogated:')
            for gated in gated_objectives:
                gated_objective_index = int(self._lib.re_sub(r'^Ogated:', '', gated))
                bad_gated_conditions = False
                for hardreq in hard_required_objectives:
                    hard_required_index = int(self._lib.re_sub(r'^Ohardreq:', '', hardreq))
                    if hard_required_index == gated_objective_index:
                        bad_gated_conditions = True
                        self._lib.push(log, ['error', f'Cannot have objective #{hard_required_index} be both gated AND hard required.'])
                        break
                doors_entrances_rando = flagset.get_list(r'^-(doors|entrances)rando:')
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

            # check for conflict between objective required characters and available ones
            char_objective_flags = flagset.get_list(r'^O\d+:char_')
            if len(char_objective_flags) > 0:
                required_chars = []
                for f in char_objective_flags:
                    ch = self._lib.re_sub(r'^O\d+:char_', '', f)
                    self._lib.push(required_chars, ch)

                if flagset.has('Cvanilla'):
                    has_unavailable_characters = False
                    if 'cecil' in required_chars:
                        has_unavailable_characters = True
                    if (flagset.has('Cnofree') and not flagset.has('Ctreasure:free')):
                        if 'edward' in required_chars or 'tellah' in required_chars or 'palom' in required_chars or 'porom' in required_chars:
                            has_unavailable_characters = True
                    if (flagset.has('Cnoearned') and not flagset.has('Ctreasure:earned')):
                        if 'rydia' in required_chars or 'kain' in required_chars or 'rosa' in required_chars or 'yang' in required_chars or 'cid' in required_chars or 'edge' in required_chars or 'fusoya' in required_chars:
                            has_unavailable_characters = True

                    if has_unavailable_characters:
                        self._lib.push(log, ['error', "Character objectives are set for characters that cannot be found in vanilla character assignment"])
                else:
                    only_flags = flagset.get_list(r'^Conly:')
                    pool = []
                    if len(only_flags) > 0:
                        for f in only_flags:
                            ch = self._lib.re_sub(r'^Conly:', '', f)
                            self._lib.push(pool, ch)
                    else:
                        pool = ['cecil', 'kain', 'rydia', 'edward', 'tellah', 'rosa', 'yang', 'palom', 'porom', 'cid', 'edge', 'fusoya']
                        for f in flagset.get_list(r'^Cno:'):
                            ch = self._lib.re_sub(r'^Cno:', '', f)
                            self._lib.remove(pool, ch)

                    for ch in required_chars:
                        if ch not in pool:
                            self._lib.push(log, ['error', "Character objectives are set for characters excluded from the randomization."])
                            break

                    distinct_flags = flagset.get_list(r'^Cdistinct:')
                    if len(distinct_flags) > 0:
                        distinct_count = int(self._lib.re_sub(r'^Cdistinct:', '', distinct_flags[0]))
                        if distinct_count < len(required_chars):
                            self._lib.push(log, ['error', "More character objectives are set than distinct characters allowed in the randomization."])

                if flagset.has('Cnofree') and flagset.has('Cnoearned') and not (flagset.has('Ctreasure:free') or flagset.has('Ctreasure:earned')):
                    self._lib.push(log, ['error', "Character objectives are set while no character slots will be filled"])                           
            
            for random_prefix in ['Orandom:char', 'Orandom2:char', 'Orandom3:char']:    
                if flagset.has(random_prefix) and flagset.has('Cnoearned') and flagset.has('Cnofree') and not flagset.has('Ctreasure:free') and not flagset.has('Ctreasure:earned'):
                    flagset.unset(random_prefix)
                    self._lib.push(log, ['correction', f'Random character objectives in the pool while no character slots will be filled. Removed {random_prefix}.'])
                    
            # remove random quest type specifiers if no random objectives specified
            for random_prefix in ['Orandom:', 'Orandom2:', 'Orandom3:']:
                if len(flagset.get_list(f'^{random_prefix}' + r'\d')) == 0:
                    self._simple_disable_regex(flagset, log, f'No random objectives specified for pool {random_prefix}', f'^{random_prefix}'+ r'[^\d]')

            total_potential_bosses = 0
            total_objective_count = 0
            for random_prefix in ['Orandom:', 'Orandom2:', 'Orandom3:']:
                if len(flagset.get_list(f'^{random_prefix}')) == 0:
                    continue
                all_customized_random_flags = flagset.get_list(f'^{random_prefix}'+ r'[^\d]')
                num_random_objectives = flagset.get_list(f'^{random_prefix}'+ r'[\d]')
                if len(num_random_objectives) == 0:
                    continue

                flag_suffix = self._lib.re_sub(f'^{random_prefix}', '', num_random_objectives[0])
                if len(all_customized_random_flags) == 0 or f'{random_prefix}boss' in all_customized_random_flags:                                        
                    total_potential_bosses += int(flag_suffix)
                total_objective_count += int(flag_suffix)
            specific_boss_objectives = flagset.get_list(r'^O[\d]:boss_')
            all_specific_objectives = flagset.get_list(r'^O[\d]:')
            total_potential_bosses += len(specific_boss_objectives)
            total_objective_count += len(all_specific_objectives)
            if flagset.has('Omode:fiends'):
                total_potential_bosses += 6
                total_objective_count += 6
            boss_collector_flags = flagset.get_suffix('Omode:bosscollector')
            if boss_collector_flags:
                boss_collector_flags = int(boss_collector_flags)
                while total_potential_bosses < boss_collector_flags:
                    total_potential_bosses += 1
            if flagset.has('Omode:classicforge'):
                total_objective_count += 1
            if flagset.has('Omode:classicgiant'):
                total_objective_count += 1
            if len(flagset.get_list(r'^Omode:dkmatter')) > 0:
                total_objective_count += 1
            if len(flagset.get_list(r'^Omode:ki')) > 0:
                total_objective_count += 1
            if len(flagset.get_list(r'^Omode:goldhunter')) > 0:
                total_objective_count += 1
            if flagset.has('Omode:external'):
                total_objective_count += 1

            max_bosses = 34
            boss_slots_removed = 0
            removed_bosses_flags = flagset.get_list(rf'^Bremove:')
            for slot in removed_bosses_flags:
                max_bosses -= 1
                boss_slots_removed += 1
            if total_potential_bosses > max_bosses:
                if boss_slots_removed > 0:
                    self._lib.push(log, ['error', f"More than {max_bosses} potential bosses specified ({boss_slots_removed} removed)"])        
                else:
                    self._lib.push(log, ['error', f"More than 34 potential bosses specified"])

            if total_objective_count > 32:
                self._lib.push(log, ['error', "More than 32 objectives specified"])                           
            #print(f'Total potential bosses is {total_potential_bosses} Objectives is {total_objective_count}')            

            # test if # of random req quests exceeds the random only characters count
            # test if the total amount of avail chararcters exceeds the required_character_count
            # test if there are enough slots for all mandatory character objectives (between Od: ones and OrandomD:char ones)
            duplicate_check_count = 0
            character_pool = []
            nonstarting_character_slots = 16
            if flagset.has('Cnofree') and not flagset.has('Ctreasure:free'):
                nonstarting_character_slots -= 5
            if flagset.has('Cnoearned') and not flagset.has('Ctreasure:earned'):
                nonstarting_character_slots -= 11
            elif flagset.has('Omode:classicforge'):
                nonstarting_character_slots -= 1
            mandatory_char_objective_slots = len(char_objective_flags)

            for random_prefix in ['Orandom:', 'Orandom2:', 'Orandom3:']:                         
                if len(flagset.get_list(f'^{random_prefix}')) == 0:
                    continue

                random_only_char_flags = flagset.get_list(f'{random_prefix}only')
                if not flagset.has(f'{random_prefix}char') and len(random_only_char_flags) > 0:
                    flagset.set(f'{random_prefix}char')
                    self._lib.push(log, ['correction', f'Random objectives requiring specific characters set without Orandom:char; setting {random_prefix}char'])

                # if this random group cannot choose character objectives, or if it can but it has many other options,
                # skip the next part where we make restrictions based on possible character objectives running out
                all_customized_random_flags = flagset.get_list(f'^{random_prefix}'+ r'[^\d]')
                if len(all_customized_random_flags) != 1 or f'{random_prefix}char'not in all_customized_random_flags:
                    continue

                all_random_flags = flagset.get_list(f'^{random_prefix}')                
                skip_pools = False
                
                for random_flag in all_random_flags:
                    flag_suffix = self._lib.re_sub(f'^{random_prefix}', '', random_flag)
                    if self._lib.re_test(r'\d', flag_suffix):
                        required_random_objective_count = int(flag_suffix)
                    elif not self._lib.re_test(r'only', flag_suffix) and not self._lib.re_test(r'char', flag_suffix):
                        skip_pools = True
                        break
                # this objective group can only pick character objectives, so add to the total
                mandatory_char_objective_slots += required_random_objective_count
                                
                duplicate_char_count = 0
                desired_char_count = 0
                # objective_rando can handle filling in a random pool with boss or quest objectives; just not if only character objectives are specified
                if len(random_only_char_flags) > 0 and len(random_only_char_flags) < required_random_objective_count and skip_pools == False:
                    self._lib.push(log, ['error', f'Random objectives requiring fewer specific characters ({len(random_only_char_flags)}) than number of objectives ({required_random_objective_count})'])
                    break
                elif len(random_only_char_flags) > 0 :
                    for random_flag in random_only_char_flags:
                        desired_char_count += 1
                        current_char = random_flag[len(f'{random_prefix}only'):]
                        if current_char not in character_pool:
                            self._lib.push(character_pool, current_char)
                        else:
                            duplicate_char_count+=1
                else:
                    all_character_pool = ['cecil', 'kain', 'rydia', 'edward', 'tellah', 'rosa', 'yang', 'palom', 'porom', 'cid', 'edge', 'fusoya']
                    desired_char_count = len(all_character_pool)
                    for current_char in all_character_pool:
                        if current_char not in character_pool:
                            self._lib.push(character_pool, current_char)
                        else:
                            duplicate_char_count+=1
                chars_to_remove = duplicate_check_count                
                if duplicate_char_count < duplicate_check_count:
                    chars_to_remove = duplicate_char_count
                actual_available_characters = desired_char_count - chars_to_remove
                #print (f'actual_available_characters {actual_available_characters} desired_char_count {desired_char_count} chars_to_remove {chars_to_remove} duplicate_char_count {duplicate_char_count} duplicate_check_count {duplicate_check_count}')
                if actual_available_characters < required_random_objective_count and skip_pools == False:
                    self._lib.push(log, ['error', f'Not enough unique characters for pool {random_prefix}.  Another pool could potentially consume some or all of these characters {random_only_char_flags}'])
                    break
                duplicate_check_count += required_random_objective_count

            # ensure that there are actually enough character slots being filled to satisfy the objective requirements
            if mandatory_char_objective_slots > nonstarting_character_slots:
                self._lib.push(log, ['error', f'Not enough available non-starting character slots for all of the mandatory character objectives specified (between fixed objectives and random pools). Either add more character slots back in, remove character objectives, or allow other objective types for some random pools.'])
            elif flagset.has('Cvanilla'):
                # on Cvanilla, we know exactly which characters are in the seed, so we need to cap the number of character objectives
                # at how many distinct characters there are.
                available_vanilla_chars = 11
                if (flagset.has('Cnofree') and not flagset.has('Ctreasure:free')):
                    available_vanilla_chars -= 4
                if (flagset.has('Cnoearned') and not flagset.has('Ctreasure:earned')):
                    available_vanilla_chars -= 7
                if mandatory_char_objective_slots > available_vanilla_chars:
                    self._lib.push(log, ['error', f'Not enough available non-starting vanilla characters for all of the mandatory character objectives specified (between fixed objectives and random pools). Either add more character slots back in, remove character objectives, or allow other objective types for some random pools.'])
            else: 
                distinct_flags = flagset.get_list(r'^Cdistinct:')
                if len(distinct_flags) > 0:
                    # we've already ensured that *specified* objective characters are available, but we need to ensure that the random objectives
                    # don't insist on too many other characters
                    distinct_count =  int(self._lib.re_sub(r'^Cdistinct:', '', distinct_flags[0]))
                    if mandatory_char_objective_slots > distinct_count:
                        self._lib.push(log, ['error', f'Too few distinct characters specified for the mandatory character objectives. Either increase the number of distinct characters, or remove character objectives.'])
                
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


