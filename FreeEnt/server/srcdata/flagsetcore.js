var _pj;
function _pj_snippets(container) {
    function in_es6(left, right) {
        if (((right instanceof Array) || ((typeof right) === "string"))) {
            return (right.indexOf(left) > (- 1));
        } else {
            if (((right instanceof Map) || (right instanceof Set) || (right instanceof WeakMap) || (right instanceof WeakSet))) {
                return right.has(left);
            } else {
                return (left in right);
            }
        }
    }
    container["in_es6"] = in_es6;
    return container;
}
_pj = {};
_pj_snippets(_pj);
class FlagSetCore {
    constructor(flagspec, lib) {
        this._flagspec = flagspec;
        this._lib = lib;
        this._flags = {};
        this._embedded_version = null;
    }
    load(flag_string) {
        if (((flag_string.length > 0) && (flag_string[0] === "b"))) {
            this._load_binary(flag_string);
        } else {
            this._load_text(flag_string);
        }
    }
    _load_text(flag_string) {
        var index, m, subflag_prefix, subflags, superflag;
        this._flags = {};
        this._embedded_version = null;
        index = 0;
        superflag = null;
        flag_string = this._lib.re_sub("\\s", "", flag_string);
        while ((flag_string.length > 0)) {
            m = this._lib.re_search("^[A-Z]", flag_string);
            if (m) {
                superflag = m[0];
                flag_string = flag_string.slice(superflag.length);
                continue;
            }
            m = this._lib.re_search("^-[a-z0-9_]+:?", flag_string);
            if (m) {
                superflag = m[0];
                flag_string = flag_string.slice(superflag.length);
                if ((! this._lib.re_test("\\:$", superflag))) {
                    this.set(superflag);
                }
                continue;
            }
            m = this._lib.re_search("^([a-z0-9_]+:)?([a-z0-9_]+(,[a-z0-9_]+)*)/?", flag_string);
            if (m) {
                if ((superflag === null)) {
                    throw new Error(`Parse error: found subflag without superflag around '${m[0]}'`);
                }
                subflag_prefix = (m[1] ? m[1] : "");
                subflags = m[2].split(",");
                for (var i = 0, _pj_a = subflags.length; (i < _pj_a); i += 1) {
                    this.set(((superflag + subflag_prefix) + subflags[i]));
                }
                flag_string = flag_string.slice(m[0].length);
                continue;
            }
            throw new Error(`Parse error around '${flag_string}'`);
        }
    }
    _load_binary(binary_string) {
        var bit_index, byte_index, byte_list, embedded_version_string, field_size, flag_binary_info, spec_version_string, src_byte, subfield_size, value, value_bit_index;
        binary_string = binary_string.slice(1);
        byte_list = this._lib.b64decode(binary_string);
        if ((byte_list.length < 3)) {
            throw new Error("Binary flag string too short");
        }
        this._embedded_version = byte_list.slice(0, 3);
        for (var i = 0, _pj_a = 3; (i < _pj_a); i += 1) {
            if ((this._embedded_version[i] !== this._flagspec["version"][i])) {
                embedded_version_string = this._lib.join(function () {
    var _pj_b = [], _pj_c = embedded_version_string;
    for (var _pj_d = 0, _pj_e = _pj_c.length; (_pj_d < _pj_e); _pj_d += 1) {
        var v = _pj_c[_pj_d];
        _pj_b.push(v.toString());
    }
    return _pj_b;
}
.call(this), ".");
                spec_version_string = this._lib.join(function () {
    var _pj_b = [], _pj_c = this._flagspec["version"];
    for (var _pj_d = 0, _pj_e = _pj_c.length; (_pj_d < _pj_e); _pj_d += 1) {
        var v = _pj_c[_pj_d];
        _pj_b.push(v.toString());
    }
    return _pj_b;
}
.call(this), ".");
                throw new Error(`Version mismatch: flag string is v${embedded_version_string}, expected v${spec_version_string}`);
            }
        }
        byte_list = byte_list.slice(3);
        this._flags = {};
        for (var i = 0, _pj_a = this._flagspec["binary"].length; (i < _pj_a); i += 1) {
            flag_binary_info = this._flagspec["binary"][i];
            field_size = flag_binary_info["size"];
            byte_index = (flag_binary_info["offset"] >> 3);
            bit_index = (flag_binary_info["offset"] & 7);
            value = 0;
            value_bit_index = 0;
            while ((field_size > 0)) {
                subfield_size = this._lib.min(field_size, (8 - bit_index));
                src_byte = ((byte_index < byte_list.length) ? byte_list[byte_index] : 0);
                value = (value | (((src_byte >> bit_index) & ((1 << subfield_size) - 1)) << value_bit_index));
                value_bit_index += subfield_size;
                field_size -= subfield_size;
                byte_index += 1;
                bit_index = 0;
            }
            if ((value === flag_binary_info["value"])) {
                this.set(flag_binary_info["flag"]);
            }
        }
    }
    get_list(regex = null) {
        var flags;
        flags = [];
        for (var flag, _pj_c = 0, _pj_a = this._flagspec["order"], _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            flag = _pj_a[_pj_c];
            if (this.has(flag)) {
                if (((regex === null) || this._lib.re_test(regex, flag))) {
                    this._lib.push(flags, flag);
                }
            }
        }
        return flags;
    }
    get_suffix(flag_prefix) {
        var flag_regex, flags;
        flag_regex = ("^" + flag_prefix);
        flags = this.get_list(flag_regex);
        if ((flags.length > 0)) {
            return flags[0].slice(flag_prefix.length);
        } else {
            return null;
        }
    }
    get_version() {
        return this._embedded_version;
    }
    has(flag) {
        if ((! _pj.in_es6(flag, this._flagspec["order"]))) {
            throw new Error(`Invalid flag ${flag}`);
        }
        if (_pj.in_es6(flag, this._flagspec["implicit"])) {
            return this._evaluate_condition(this._flagspec["implicit"][flag]);
        } else {
            if (_pj.in_es6(flag, this._flags)) {
                return true;
            } else {
                return false;
            }
        }
    }
    has_any(...flags) {
        for (var flag, _pj_c = 0, _pj_a = flags, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            flag = _pj_a[_pj_c];
            if (this.has(flag)) {
                return true;
            }
        }
        return false;
    }
    has_all(...flags) {
        for (var flag, _pj_c = 0, _pj_a = flags, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            flag = _pj_a[_pj_c];
            if ((! this.has(flag))) {
                return false;
            }
        }
        return true;
    }
    set(flag) {
        if (_pj.in_es6(flag, this._flagspec["implicit"])) {
            return;
        }
        for (var mutex_set, _pj_c = 0, _pj_a = this._flagspec["mutex"], _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            mutex_set = _pj_a[_pj_c];
            if (_pj.in_es6(flag, mutex_set)) {
                for (var other_flag, _pj_f = 0, _pj_d = mutex_set, _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                    other_flag = _pj_d[_pj_f];
                    if ((other_flag !== flag)) {
                        this.unset(other_flag);
                    }
                }
                break;
            }
        }
        this._flags[flag] = true;
    }
    unset(flag) {
        if (_pj.in_es6(flag, this._flags)) {
            delete this._flags[flag];
        }
    }
    parse() {
        var m, results, subflag, subflag_obj, subsubflag, superflag, superflag_obj;
        results = [];
        for (var flag, _pj_c = 0, _pj_a = this._flagspec["order"], _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            flag = _pj_a[_pj_c];
            if ((! this.has(flag))) {
                continue;
            }
            if ((flag[0] === "-")) {
                m = this._lib.re_search("^(-[a-z0-9_]+:?)([a-z0-9_]+)?$", flag);
                superflag = m[1];
                subflag = m[2];
                subsubflag = null;
            } else {
                m = this._lib.re_search("^([A-Z])(([a-z0-9_]+:)?([a-z0-9_]+))?$", flag);
                superflag = m[1];
                subflag = (m[3] ? m[3] : m[4]);
                subsubflag = (m[3] ? m[4] : null);
            }
            superflag_obj = null;
            for (var item, _pj_f = 0, _pj_d = results, _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                item = _pj_d[_pj_f];
                if ((item[0] === superflag)) {
                    superflag_obj = item;
                    break;
                }
            }
            if ((! superflag_obj)) {
                superflag_obj = [superflag, []];
                this._lib.push(results, superflag_obj);
            }
            if (subflag) {
                subflag_obj = null;
                for (var item, _pj_f = 0, _pj_d = superflag_obj[1], _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                    item = _pj_d[_pj_f];
                    if ((item[0] === subflag)) {
                        subflag_obj = item;
                        break;
                    }
                }
                if ((! subflag_obj)) {
                    subflag_obj = [subflag, []];
                    this._lib.push(superflag_obj[1], subflag_obj);
                }
                if (subsubflag) {
                    this._lib.push(subflag_obj[1], subsubflag);
                }
            }
        }
        return results;
    }
    _evaluate_condition(condition) {
        if (this._lib.is_string(condition)) {
            return this.has(condition);
        } else {
            if ((condition[0] === "not")) {
                return (! this._evaluate_condition(condition[1]));
            } else {
                if ((condition[0] === "and")) {
                    for (var subcondition, _pj_c = 0, _pj_a = condition.slice(1), _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                        subcondition = _pj_a[_pj_c];
                        if ((! this._evaluate_condition(subcondition))) {
                            return false;
                        }
                    }
                    return true;
                } else {
                    if ((condition[0] === "or")) {
                        for (var subcondition, _pj_c = 0, _pj_a = condition.slice(1), _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                            subcondition = _pj_a[_pj_c];
                            if (this._evaluate_condition(subcondition)) {
                                return true;
                            }
                        }
                        return false;
                    } else {
                        throw new Error(`Unsupported condition type ${condition[0]}`);
                    }
                }
            }
        }
    }
    _wrap(text, first_line_width, paragraph_width) {
        var break_index, line_width, lines;
        line_width = first_line_width;
        lines = [];
        while ((text.length > line_width)) {
            break_index = line_width;
            for (var i = (line_width - 1), _pj_a = (- 1); (i < _pj_a); i += (- 1)) {
                if ((((text[i] === ",") || (text[i] === ")")) || (text[i] === " "))) {
                    break_index = (i + 1);
                    break;
                }
            }
            this._lib.push(lines, text.slice(0, break_index));
            text = text.slice(break_index);
            line_width = paragraph_width;
        }
        if ((text.length > 0)) {
            this._lib.push(lines, text);
        }
        return lines;
    }
    to_string(pretty = false, wrap_width = null) {
        var last_superflag, line, lines, paragraph_indent, parsed, parts, prefix, segment, subflag_obj_index, subflag_obj_list, sublines, subsubflags, superflag, superflag_last_index, superflag_prefix;
        parsed = this.parse();
        parts = [];
        lines = [];
        last_superflag = null;
        for (var superflag_obj, _pj_c = 0, _pj_a = parsed, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            superflag_obj = _pj_a[_pj_c];
            if (((! pretty) && (parts.length > 0))) {
                this._lib.push(parts, " ");
            } else {
                if (((pretty && (lines.length > 0)) && (last_superflag[0] !== "-"))) {
                    this._lib.push(lines, "");
                }
            }
            superflag = superflag_obj[0];
            last_superflag = superflag;
            superflag_last_index = (superflag.length - 1);
            superflag_prefix = (superflag + ((pretty && (superflag[superflag_last_index] !== ":")) ? " " : ""));
            this._lib.push(parts, superflag_prefix);
            if ((superflag_obj[1].length > 0)) {
                if ((superflag[0] === "-")) {
                    subsubflags = [];
                    for (var subflag_obj, _pj_f = 0, _pj_d = superflag_obj[1], _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                        subflag_obj = _pj_d[_pj_f];
                        this._lib.push(subsubflags, subflag_obj[0]);
                    }
                    subflag_obj_list = [["", subsubflags]];
                } else {
                    subflag_obj_list = superflag_obj[1];
                }
                subflag_obj_index = 0;
                for (var subflag_obj, _pj_f = 0, _pj_d = subflag_obj_list, _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                    subflag_obj = _pj_d[_pj_f];
                    if ((pretty && (parts.length === 0))) {
                        this._lib.push(parts, " /");
                    }
                    segment = (subflag_obj[0] + this._lib.join(subflag_obj[1], ","));
                    if (pretty) {
                        this._lib.push(parts, segment);
                        paragraph_indent = "   ";
                        line = this._lib.join(parts, "");
                        if ((wrap_width === null)) {
                            sublines = [line];
                        } else {
                            sublines = this._wrap(line, wrap_width, (wrap_width - paragraph_indent.length));
                        }
                        prefix = "";
                        for (var subline, _pj_i = 0, _pj_g = sublines, _pj_h = _pj_g.length; (_pj_i < _pj_h); _pj_i += 1) {
                            subline = _pj_g[_pj_i];
                            this._lib.push(lines, (prefix + subline));
                            prefix = paragraph_indent;
                        }
                        parts = [];
                    } else {
                        if ((subflag_obj_index > 0)) {
                            this._lib.push(parts, "/");
                        }
                        this._lib.push(parts, segment);
                    }
                    subflag_obj_index += 1;
                }
            } else {
                if (pretty) {
                    this._lib.push(lines, parts[0]);
                    parts = [];
                }
            }
        }
        if ((! pretty)) {
            line = this._lib.join(parts, "");
            if ((wrap_width !== null)) {
                line = this._lib.join(this._wrap(line, wrap_width, wrap_width), "\n");
            }
            return line;
        } else {
            return this._lib.join(lines, "\n");
        }
    }
    to_binary() {
        var bit_index, byte_index, byte_list, dst_byte, field_size, subfield_size, subvalue, value;
        byte_list = [];
        for (var i = 0, _pj_a = 3; (i < _pj_a); i += 1) {
            this._lib.push(byte_list, this._flagspec["version"][i]);
        }
        for (var flag_binary_info, _pj_c = 0, _pj_a = this._flagspec["binary"], _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            flag_binary_info = _pj_a[_pj_c];
            if ((! this.has(flag_binary_info["flag"]))) {
                continue;
            }
            value = flag_binary_info["value"];
            field_size = flag_binary_info["size"];
            byte_index = ((flag_binary_info["offset"] >> 3) + 3);
            bit_index = (flag_binary_info["offset"] & 7);
            while ((field_size > 0)) {
                while ((byte_index >= byte_list.length)) {
                    this._lib.push(byte_list, 0);
                }
                dst_byte = byte_list[byte_index];
                subfield_size = this._lib.min(field_size, (8 - bit_index));
                subvalue = (value & ((1 << subfield_size) - 1));
                byte_list[byte_index] = (dst_byte | (subvalue << bit_index));
                value >>= subfield_size;
                field_size -= subfield_size;
                bit_index = 0;
                byte_index += 1;
            }
        }
        return ("b" + this._lib.b64encode(byte_list));
    }
}
class FlagLogicCore {
    constructor(flagspec, lib) {
        this._flagspec = flagspec;
        this._lib = lib;
    }
    _simple_disable(flagset, log, prefix, flags_to_disable) {
        for (var flag, _pj_c = 0, _pj_a = flags_to_disable, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            flag = _pj_a[_pj_c];
            if (flagset.has(flag)) {
                flagset.unset(flag);
                console.log(((prefix + "; removed ") + flag));
                this._lib.push(log, ["correction", ((prefix + "; removed ") + flag)]);
            }
        }
    }
    _simple_disable_regex(flagset, log, prefix, flags_regex) {
        this._simple_disable(flagset, log, prefix, flagset.get_list(flags_regex));
    }
    fix(flagset) {
        var WACKY_SET_1, WACKY_SET_2, WACKY_SET_3, actual_available_characters, all_customized_rand_flags, all_customized_random_flags, all_specific_objectives, all_spoiler_flags, available_vanilla_chars, bad_gated_conditions, boss, boss_slots_removed, bosses_available, ch, ch_count_cap, ch_list, challenges, char_objective_flags, character_pool, current_boss, distinct_count, distinct_flags, doors_entrances_rando, duplicate_char_count, fl_cat, flags_objective_chars, flags_objective_chars_num, flexible_char_count, flexible_char_pool, flexible_random_objective_count, gated_objective_index, gated_objectives, group_obj_num, group_scores, grp_obj_num, grp_sc, hard_required_index, hard_required_objectives, has_unavailable_characters, just_in_case_mandatory_char_pool, kmiab_flags, log, max_bosses, max_char_objectives, max_non_tough_quests, max_tough_quests, min_non_char_objectives, mode, non_tough_quest_room, nonstarting_character_slots, num_rand_objectives, num_random_objectives, only_char_objectives, only_chars_list, only_flags, pass_quest_flags, qu, rand_category_flags, rand_only_char_flags, random_category_flags, random_only_char_flags, removed_bosses_flags, required_chars, required_count, required_objective_count, sorted_groups, sparse_spoiler_flags, specific_boss_objectives, specific_tough_quest_objectives, start_exclude_flags, start_include_flags, theoretical_available_characters, total_char_count, total_flexible_bosses, total_flexible_non_tough_quests, total_flexible_tough_quests, total_mandatory_bosses, total_mandatory_non_tough_quests, total_mandatory_tough_quests, total_objective_count, tough_quest_room, unsure_flags, win_flags;
        log = [];
        if ((flagset.has("Kunsafer") && (! flagset.has_any("Ksummon", "Kmoon", "Kmiab:above", "Kmiab:lst", "Kmiab:standard", "Kmiab:all")))) {
            flagset.set("Kmoon");
            this._lib.push(log, ["correction", "Kunsafer requires placing key items on the moon/Giant, and Knofree does not count; adding Kmoon (but you can instead add any Darkness-locked checks)"]);
        }
        if ((flagset.has("Kforge") && flagset.has("Omode:classicforge"))) {
            this._simple_disable(flagset, log, "Classic forge is incompatible with Kforge", ["Kforge"]);
        }
        if (flagset.has("Kforge")) {
            this._simple_disable_regex(flagset, log, "-smith is incompatible with Kforge", "^-smith:");
        }
        if ((flagset.has_any("Ksummon", "Kmoon", "Kforge", "Kpink", "Kmiab:standard", "Kmiab:above", "Kmiab:below", "Kmiab:lst", "Kmiab:all") && (! flagset.has("Kmain")))) {
            flagset.set("Kmain");
            this._lib.push(log, ["correction", "Advanced key item randomizations are enabled; forced to add Kmain"]);
        }
        if ((flagset.has("Owin:crystal") && flagset.has("Omode:ki17"))) {
            flagset.unset("Omode:ki17");
            flagset.set("Omode:ki16");
            this._lib.push(log, ["correction", "Can only collect 16 KIs for an objective with Owin:crystal; changing Omode:ki17 to Omode:ki16"]);
        }
        if (((! flagset.has_any("Ksummon", "Kmoon", "Kforge", "Kpink", "Kmiab:standard", "Kmiab:above", "Kmiab:below", "Kmiab:lst", "Kmiab:all")) && flagset.has("Omode:ki17"))) {
            this._simple_disable(flagset, log, "Cannot replace a key item if all of them are required", ["Pkey", "Kstart:pass"]);
            this._simple_disable(flagset, log, "Cannot remove a key item reward slot if all of them are required", ["Kstart:zonk"]);
        }
        if (((((! flagset.has_any("Ksummon", "Kmoon", "Kforge", "Kpink", "Kmiab:standard", "Kmiab:above", "Kmiab:below", "Kmiab:lst", "Kmiab:all")) && flagset.has("Pkey")) && (! flagset.has("Owin:crystal"))) && flagset.has("Omode:ki16"))) {
            this._simple_disable(flagset, log, "Cannot remove two key items if one of them is required", ["Kstart:zonk"]);
        }
        if (flagset.has("Kvanilla")) {
            this._simple_disable(flagset, log, "Key items not randomized", ["Kunsafe", "Kunsafer", "Kunweighted"]);
            this._simple_disable_regex(flagset, log, "Key items not randomized", "^Kstart:");
        }
        if (flagset.has("Kstart:darkness")) {
            this._simple_disable(flagset, log, "Klatedark is incompatible with starting with Darkness", ["Klatedark"]);
        }
        if (flagset.has("Klatedark")) {
            this._simple_disable(flagset, log, "Klatedark implicitly guarantees safe underground access", ["Kunsafe", "Kunsafer"]);
        }
        if ((flagset.has("Kstart:pass") && (! flagset.has("Pkey")))) {
            flagset.set("Pkey");
            this._lib.push(log, ["correction", "Kstart:pass implies Pkey"]);
        }
        kmiab_flags = flagset.get_list("^Kmiab:");
        if ((_pj.in_es6("Kmiab:all", kmiab_flags) && (kmiab_flags.length > 1))) {
            this._simple_disable_regex(flagset, log, "All miabs already included", "^Kmiab:(standard|above|below|lst)");
        } else {
            if ((_pj.in_es6("Kmiab:standard", kmiab_flags) && (kmiab_flags.length > 1))) {
                this._simple_disable_regex(flagset, log, "Standard miab inclusion takes priority", "^Kmiab:(above|below|lst)");
            }
        }
        if (flagset.has("Cvanilla")) {
            this._simple_disable_regex(flagset, log, "Characters not randomized", "^C(maybe|distinct:|only:|no:)");
        } else {
            only_flags = flagset.get_list("^Conly:");
            if ((only_flags.length > 0)) {
                this._simple_disable_regex(flagset, log, "Conly:* flag(s) are specified", "^Cno:");
            }
        }
        if (flagset.has("Chero")) {
            this._simple_disable_regex(flagset, log, "Hero challenge includes smith weapon", "^-smith:(super|alt|playable)");
            if (flagset.has("Aagnostic")) {
                flagset.set("Ahero");
                this._lib.push(log, ["correction", "In the absence of other agility flags, Chero implies Ahero; replaced Aagnostic with Ahero"]);
            }
        }
        start_include_flags = flagset.get_list("^Cstart:(?!not_)");
        start_exclude_flags = flagset.get_list("^Cstart:not_");
        if (((start_exclude_flags.length > 0) && (start_include_flags.length > 0))) {
            this._simple_disable_regex(flagset, log, "Inclusive Cstart:* flags are specified", "^Cstart:not_");
        }
        if (((start_include_flags.length > 1) && flagset.has("Cstart:any"))) {
            this._simple_disable_regex(flagset, log, "Cstart:any is specified", "^Cstart:(?!any|not_)");
        }
        if ((flagset.has("Kstart:magma") && flagset.has("Kforce:hook"))) {
            this._simple_disable_regex(flagset, log, "Force hook with start:Magma", "^Kforce:hook");
        }
        if ((flagset.has("Cnekkie") && (flagset.get_list("^Cthrift:").length > 0))) {
            this._simple_disable_regex(flagset, log, "Starting gear specified by Cnekkie", "^Cthrift:");
        }
        if (((flagset.has("Ctreasure:unsafe") || flagset.has("Ctreasure:relaxed")) && (! (flagset.has("Ctreasure:free") || flagset.has("Ctreasure:earned"))))) {
            flagset.set("Ctreasure:free");
            flagset.set("Ctreasure:earned");
            this._lib.push(log, ["correction", "Ctreasure:unsafe/wild set, auto-assigning Ctreasure:free and Ctreasure:earned"]);
        }
        if ((flagset.get_list("^Ctreasure:") && ((flagset.has("Tvanilla") || flagset.has("Tshuffle")) || flagset.has("Tempty")))) {
            this._simple_disable_regex(flagset, log, "Ctreasure: with vanilla, shuffled, or empty chests", "^Ctreasure:");
        }
        if ((flagset.has("Ctreasure:earned") && (! flagset.has("Cnoearned")))) {
            flagset.set("Cnoearned");
            this._lib.push(log, ["correction", "Ctreasure:earned set, auto-assigning Cnoearned"]);
        }
        if ((flagset.has("Ctreasure:free") && (! flagset.has("Cnofree")))) {
            flagset.set("Cnofree");
            this._lib.push(log, ["correction", "Ctreasure:free set, auto-assigning Cnofree"]);
        }
        if (flagset.has("Tempty")) {
            this._simple_disable_regex(flagset, log, "Treasures are empty", "^Tsparse:");
        }
        if ((flagset.get_list("^Tsparsey:") && (! flagset.get_list("^Tsparse:")))) {
            this._simple_disable_regex(flagset, log, "Tsparsey specified without Tsparse", "^Tsparsey:");
        }
        if (flagset.has_any("Tempty", "Tvanilla", "Tshuffle")) {
            this._simple_disable_regex(flagset, log, "Treasures are not random", "^Tmaxtier:");
            this._simple_disable_regex(flagset, log, "Treasures are not random", "^Tmintier:");
        }
        if ((flagset.has("Tadjmiabareas") && (! flagset.has_any("Tpro", "Tsemipro", "Twildish", "Tvanillaish", "Tstandardish")))) {
            this._simple_disable(flagset, log, "Treasures are not weighted", ["Tadjmiabareas"]);
        }
        if (flagset.has_any("Svanilla", "Sshuffle", "Scabins", "Sempty")) {
            this._simple_disable_regex(flagset, log, "Shops are not random", "^(Sno:([^j]|j.)|Salways:([^j]|j.))");
            if ((! flagset.has("Sshuffle"))) {
                this._simple_disable(flagset, log, "Shops are not random", ["Sunsafe"]);
            }
        }
        for (var f, _pj_c = 0, _pj_a = ["apples", "sirens", "vampires", "hrglass", "bacchus", "starveil", "cure3", "illusion", "coffin", "damage_items"], _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            f = _pj_a[_pj_c];
            if ((flagset.has(("Salways:" + f)) && flagset.has(("Sno:" + f)))) {
                this._simple_disable(flagset, log, "Salways: overrides Sno:", [("Sno:" + f)]);
            }
        }
        if (flagset.has("Bvanilla")) {
            this._simple_disable(flagset, log, "Bosses not randomized", ["Bunsafe"]);
            this._simple_disable_regex(flagset, log, "Bosses not randomized", "^Brestrict:");
        }
        if (flagset.has("Evanilla")) {
            this._simple_disable(flagset, log, "Encounters are vanilla", ["Ekeep:behemoths", "Ekeep:doors", "Edanger"]);
        }
        if ((flagset.get_list("^-smith:(playable|good)").length === flagset.get_list("^-smith:").length)) {
            this._simple_disable(flagset, log, "No smith item requested", ["-smith:playable", "-smith:good"]);
        }
        if ((flagset.has("-smith:omni") && (! flagset.has_any("-smith:super", "Chero")))) {
            this._simple_disable(flagset, log, "No FF4A weapon available", ["-smith:omni"]);
        }
        if ((flagset.has("Fslowstart") && flagset.has("Funcapped"))) {
            this._simple_disable(flagset, log, "Uncapped FuSoYa cannot also have slowstart", ["Fslowstart"]);
        }
        if ((flagset.has("Flocation") && flagset.has("Fslowstart"))) {
            this._simple_disable(flagset, log, "Location FuSoYa cannot have slowstart", ["Fslowstart"]);
        }
        if (flagset.has("Fnerfed")) {
            this._simple_disable_regex(flagset, log, "Nerfed FuSoYa cannot have slowstart or unlearn spells", "^F(slowstart|unlearn)");
        }
        if (flagset.has("Fvanilla")) {
            this._simple_disable_regex(flagset, log, "Vanilla FuSoYa cannot have his HP or spells change", "^F(slowstart|unlearn|randomhp)");
        }
        if ((flagset.has("-monsterflee") && (! flagset.has("-monsterevade")))) {
            flagset.set("-monsterevade");
            this._lib.push(log, ["correction", "Monsters require evade to flee; forced to add -monsterevade"]);
        }
        if (flagset.has_any("-entrancesrando:normal", "-entrancesrando:gated", "-entrancesrando:blueplanet", "-entrancesrando:why", "-entrancesrando:all")) {
            this._simple_disable_regex(flagset, log, "Entrances rando takes priority", "^-doorsrando");
        }
        if ((! flagset.has_any("-entrancesrando:normal", "-entrancesrando:gated", "-entrancesrando:blueplanet", "-entrancesrando:why", "-entrancesrando:all", "-doorsrando:normal", "-doorsrando:gated", "-doorsrando:blueplanet", "-doorsrando:why", "-doorsrando:all"))) {
            this._simple_disable(flagset, log, "Removing doors rando related flags when no doors/entrances option is enabled ", ["-calmness", "-forcesealed"]);
        }
        if (flagset.has_any("-entrancesrando:normal", "-entrancesrando:gated", "-entrancesrando:blueplanet", "-entrancesrando:why", "-entrancesrando:all")) {
            this._simple_disable_regex(flagset, log, "Entrances rando takes priority", "^-doorsrando");
        }
        if ((! flagset.has_any("-entrancesrando:normal", "-entrancesrando:gated", "-entrancesrando:blueplanet", "-entrancesrando:why", "-entrancesrando:all", "-doorsrando:normal", "-doorsrando:gated", "-doorsrando:blueplanet", "-doorsrando:why", "-doorsrando:all"))) {
            this._simple_disable(flagset, log, "Removing doors rando related flags when no doors/entrances option is enabled ", ["-calmness", "-forcesealed"]);
        }
        if (flagset.has_any("-starting:underground", "-starting:blackchocobo")) {
            this._lib.push(log, ["error", "Different starting location flags are not currently available; remove them and try again."]);
        }
        unsure_flags = flagset.get_list("^Zunsure:");
        for (var fl, _pj_c = 0, _pj_a = unsure_flags, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            fl = _pj_a[_pj_c];
            fl_cat = ("Z" + this._lib.re_sub("^Zunsure:", "", fl));
            if (flagset.has(fl_cat)) {
                flagset.unset(fl);
                this._lib.push(log, ["correction", `Cannot use ${fl} when ${fl_cat} is set; removed ${fl}`]);
            }
        }
        if ((flagset.has("Zphysical") && flagset.has("Zwhichbang"))) {
            this._simple_disable(flagset, log, "No guaranteed Big Bangs in script", ["Zwhichbang"]);
        }
        if ((flagset.has_any("Zchaos", "Zlavosshell") && (! flagset.has_any("Zunsure:vanilla", "Zunsure:physical", "Zunsure:ailments")))) {
            this._simple_disable(flagset, log, "Random phases take precedence over shuffled phases", ["Zphaseshift"]);
        }
        all_spoiler_flags = flagset.get_list("^-spoil:");
        sparse_spoiler_flags = flagset.get_list("^-spoil:sparse");
        if (((all_spoiler_flags.length > 0) && (all_spoiler_flags.length === sparse_spoiler_flags.length))) {
            this._simple_disable_regex(flagset, log, "No spoilers requested", "^-spoil:sparse");
        }
        if (((flagset.has("Chi") && flagset.has("Chero")) && flagset.has("Cparty:1"))) {
            this._simple_disable(flagset, log, "No room for characters to be added with Chero and Max Party size of 1", ["Chi"]);
        }
        if (((flagset.has("Cfifo") && flagset.has("Chero")) && flagset.has("Cparty:1"))) {
            this._simple_disable(flagset, log, "Cant remove characters with Chero and Max Party size of 1", ["Cfifo"]);
        }
        if ((flagset.has("Cpermajoin") && flagset.has("Cfifo"))) {
            this._simple_disable(flagset, log, "Permajoin and Remove Oldest are incompatible", ["Cfifo"]);
        }
        if (flagset.has("-tweak:rydiaredmage")) {
            if (flagset.has_any("-call:vanillagrowup", "-call:nogrowup")) {
                this._simple_disable(flagset, log, "Rydia must learn white magic at Dwarf Castle as a Red Mage", ["-call:vanillagrowup", "-call:nogrowup"]);
            }
        }
        if (flagset.has("Onone")) {
            this._simple_disable_regex(flagset, log, "No objectives set", "^O(win|req):");
            this._simple_disable_regex(flagset, log, "No objectives set", "^Xobjectivebonus");
        } else {
            if ((flagset.get_list("^Oreq:").length === 0)) {
                flagset.set("Oreq:all");
                this._lib.push(log, ["correction", "Required number of objectives not specified; setting Oreq:all"]);
            }
            hard_required_objectives = flagset.get_list("^Ohardreq:");
            if (flagset.has("Oreq:all")) {
                if ((hard_required_objectives.length !== 0)) {
                    this._simple_disable_regex(flagset, log, "Hard required objectives found, but all objectives are already required. Removing hard required flags", "^Ohardreq:");
                    this._lib.push(log, ["correction", "Hard required objectives found, but all objectives are already required.  Ignoring hard required flags."]);
                }
            } else {
                required_count = flagset.get_list("^Oreq:");
                if ((required_count.length > 0)) {
                    required_objective_count = Number.parseInt(this._lib.re_sub("^Oreq:", "", required_count[0]));
                    if ((hard_required_objectives.length > required_objective_count)) {
                        this._simple_disable_regex(flagset, log, "Changing required count", "^Oreq:");
                        flagset.set(`Oreq:${hard_required_objectives.length}`);
                        this._lib.push(log, ["correction", `More hard required objectives set than number of objectives required, increasing required objective count to ${hard_required_objectives.length}.`]);
                    }
                }
            }
            gated_objectives = flagset.get_list("^Ogated:");
            for (var gated, _pj_c = 0, _pj_a = gated_objectives, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                gated = _pj_a[_pj_c];
                gated_objective_index = Number.parseInt(this._lib.re_sub("^Ogated:", "", gated));
                bad_gated_conditions = false;
                for (var hardreq, _pj_f = 0, _pj_d = hard_required_objectives, _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                    hardreq = _pj_d[_pj_f];
                    hard_required_index = Number.parseInt(this._lib.re_sub("^Ohardreq:", "", hardreq));
                    if ((hard_required_index === gated_objective_index)) {
                        bad_gated_conditions = true;
                        this._lib.push(log, ["error", `Cannot have objective #${hard_required_index} be both gated AND hard required.`]);
                        break;
                    }
                }
                doors_entrances_rando = flagset.get_list("^-(doors|entrances)rando:");
                for (var doors_entrances, _pj_f = 0, _pj_d = doors_entrances_rando, _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                    doors_entrances = _pj_d[_pj_f];
                    bad_gated_conditions = true;
                    this._lib.push(log, ["error", "Doors and entrances rando does not currently support gated objectives."]);
                    break;
                }
                if (bad_gated_conditions) {
                    break;
                }
            }
            win_flags = flagset.get_list("^Owin:");
            if ((flagset.has("Omode:classicforge") && (! flagset.has("Owin:crystal")))) {
                flagset.set("Owin:crystal");
                this._lib.push(log, ["correction", "Classic Forge is enabled; forced to add Owin:crystal"]);
            } else {
                if ((win_flags.length === 0)) {
                    flagset.set("Owin:game");
                    this._lib.push(log, ["correction", "Objectives set without outcome specified; added Owin:game"]);
                }
            }
            pass_quest_flags = flagset.get_list("^O\\d+:quest_pass$");
            if (((pass_quest_flags.length > 0) && flagset.has("Pnone"))) {
                flagset.set("Pkey");
                this._lib.push(log, ["correction", "Pass objective is set without a pass flag; forced to add Pkey"]);
            }
            flags_objective_chars = [];
            if (flagset.has("Cvanilla")) {
                if ((! (flagset.has("Cnofree") && (! flagset.has("Ctreasure:free"))))) {
                    for (var c, _pj_c = 0, _pj_a = ["edward", "tellah", "palom", "porom"], _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                        c = _pj_a[_pj_c];
                        this._lib.push(flags_objective_chars, c);
                    }
                }
                if ((! (flagset.has("Cnoearned") && (! flagset.has("Ctreasure:earned"))))) {
                    for (var c, _pj_c = 0, _pj_a = ["rydia", "kain", "rosa", "yang", "cid", "edge", "fusoya"], _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                        c = _pj_a[_pj_c];
                        this._lib.push(flags_objective_chars, c);
                    }
                }
                flags_objective_chars_num = flags_objective_chars.length;
            } else {
                only_flags = flagset.get_list("^Conly:");
                if ((only_flags.length > 0)) {
                    for (var f, _pj_c = 0, _pj_a = only_flags, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                        f = _pj_a[_pj_c];
                        ch = this._lib.re_sub("^Conly:", "", f);
                        this._lib.push(flags_objective_chars, ch);
                    }
                } else {
                    flags_objective_chars = ["cecil", "kain", "rydia", "edward", "tellah", "rosa", "yang", "palom", "porom", "cid", "edge", "fusoya"];
                    for (var f, _pj_c = 0, _pj_a = flagset.get_list("^Cno:"), _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                        f = _pj_a[_pj_c];
                        ch = this._lib.re_sub("^Cno:", "", f);
                        this._lib.remove(flags_objective_chars, ch);
                    }
                }
                flags_objective_chars_num = flags_objective_chars.length;
                distinct_flags = flagset.get_list("^Cdistinct:");
                if ((distinct_flags.length > 0)) {
                    distinct_count = Number.parseInt(this._lib.re_sub("^Cdistinct:", "", distinct_flags[0]));
                    while ((flags_objective_chars_num > distinct_count)) {
                        flags_objective_chars_num -= 1;
                    }
                }
            }
            char_objective_flags = flagset.get_list("^O\\d+:char_");
            character_pool = [];
            required_chars = [];
            if ((char_objective_flags.length > 0)) {
                for (var f, _pj_c = 0, _pj_a = char_objective_flags, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                    f = _pj_a[_pj_c];
                    ch = this._lib.re_sub("^O\\d+:char_", "", f);
                    this._lib.push(required_chars, ch);
                }
                has_unavailable_characters = false;
                for (var ch, _pj_c = 0, _pj_a = required_chars, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                    ch = _pj_a[_pj_c];
                    if ((! _pj.in_es6(ch, flags_objective_chars))) {
                        has_unavailable_characters = true;
                    }
                }
                if (has_unavailable_characters) {
                    if (flagset.has("Cvanilla")) {
                        this._lib.push(log, ["error", "Character objectives are set for characters that cannot be found in vanilla character assignment"]);
                    } else {
                        this._lib.push(log, ["error", "Character objectives are set for characters excluded from the randomization."]);
                    }
                }
                if ((flags_objective_chars_num < required_chars.length)) {
                    this._lib.push(log, ["error", "More character objectives are set than distinct characters allowed in the randomization."]);
                }
                if (((flagset.has("Cnofree") && flagset.has("Cnoearned")) && (! (flagset.has("Ctreasure:free") || flagset.has("Ctreasure:earned"))))) {
                    this._lib.push(log, ["error", "Character objectives are set while no character slots will be filled"]);
                }
                for (var ch, _pj_c = 0, _pj_a = required_chars, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                    ch = _pj_a[_pj_c];
                    this._lib.push(character_pool, ch);
                }
            }
            for (var random_prefix, _pj_c = 0, _pj_a = ["Orandom:", "Orandom2:", "Orandom3:"], _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                random_prefix = _pj_a[_pj_c];
                if ((((((flagset.get_list((`^${random_prefix}` + "(char|only)")).length > 0) && flagset.has("Cnoearned")) && flagset.has("Cnofree")) && (! flagset.has("Ctreasure:free"))) && (! flagset.has("Ctreasure:earned")))) {
                    this._lib.push(log, ["error", `Random character objectives specified in the ${random_prefix} pool while no character slots will be filled.`]);
                }
            }
            for (var random_prefix, _pj_c = 0, _pj_a = ["Orandom:", "Orandom2:", "Orandom3:"], _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                random_prefix = _pj_a[_pj_c];
                if ((flagset.get_list((`^${random_prefix}` + "\\d")).length === 0)) {
                    this._simple_disable_regex(flagset, log, `No random objectives specified for pool ${random_prefix}`, (`^${random_prefix}` + "[^\\d]"));
                }
            }
            if (flagset.has("Omode:classicforge")) {
                this._simple_disable_regex(flagset, log, "Classic Forge takes priority over the normal Forge quest", "^O[\\d]:quest_forge");
            }
            if (flagset.has("Omode:classicgiant")) {
                this._simple_disable_regex(flagset, log, "Classic Giant takes priority over the normal Giant quest", "^O[\\d]:quest_giant");
            }
            if (flagset.has("Omode:fiends")) {
                for (var b_fl, _pj_c = 0, _pj_a = ["milon", "kainazzo", "valvalis", "rubicant", "elements"], _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                    b_fl = _pj_a[_pj_c];
                    this._simple_disable_regex(flagset, log, `The specified boss is already an objective because of Omode:fiends`, ("^O[\\d]:boss_" + b_fl));
                }
            }
            total_mandatory_bosses = 0;
            total_flexible_bosses = 0;
            total_mandatory_tough_quests = 0;
            total_flexible_tough_quests = 0;
            total_mandatory_non_tough_quests = 0;
            total_flexible_non_tough_quests = 0;
            flexible_random_objective_count = 0;
            total_objective_count = 0;
            max_tough_quests = 22;
            max_non_tough_quests = 17;
            total_char_count = char_objective_flags.length;
            flexible_char_count = 0;
            flexible_char_pool = [];
            nonstarting_character_slots = 16;
            if ((flagset.has("Cnofree") && (! flagset.has("Ctreasure:free")))) {
                nonstarting_character_slots -= 5;
            }
            if ((flagset.has("Cnoearned") && (! flagset.has("Ctreasure:earned")))) {
                nonstarting_character_slots -= 11;
            } else {
                if (flagset.has("Omode:classicgiant")) {
                    nonstarting_character_slots -= 1;
                }
            }
            while ((flags_objective_chars_num > nonstarting_character_slots)) {
                flags_objective_chars_num -= 1;
            }
            specific_boss_objectives = [];
            for (var fl, _pj_c = 0, _pj_a = flagset.get_list("^O[\\d]:boss_"), _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                fl = _pj_a[_pj_c];
                boss = this._lib.re_sub("^O\\d+:boss_", "", fl);
                this._lib.push(specific_boss_objectives, boss);
            }
            specific_tough_quest_objectives = [];
            for (var fl, _pj_c = 0, _pj_a = flagset.get_list("^O[\\d]:quest_"), _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                fl = _pj_a[_pj_c];
                qu = this._lib.re_sub("^O\\d+:", "", fl);
                this._lib.push(specific_tough_quest_objectives, qu);
            }
            if (((! flagset.has_any("Pkey", "Pchests", "Pshop")) && (! _pj.in_es6("quest_pass", specific_tough_quest_objectives)))) {
                max_non_tough_quests -= 1;
            }
            for (var f, _pj_c = 0, _pj_a = ["quest_mistcave", "quest_waterfall", "quest_antlionnest", "quest_hobs", "quest_fabul", "quest_ordeals", "quest_baroninn", "quest_pass", "quest_dwarfcastle", "quest_lowerbabil", "quest_unlocksewer", "quest_music", "quest_toroiatreasury", "quest_magma", "quest_unlocksealedcave", "quest_bigwhale", "quest_wakeyang"], _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                f = _pj_a[_pj_c];
                if (_pj.in_es6(f, specific_tough_quest_objectives)) {
                    total_mandatory_non_tough_quests += 1;
                }
                this._lib.remove(specific_tough_quest_objectives, f);
            }
            all_specific_objectives = flagset.get_list("^O[\\d]:");
            total_mandatory_bosses += specific_boss_objectives.length;
            total_mandatory_tough_quests += specific_tough_quest_objectives.length;
            total_objective_count += all_specific_objectives.length;
            if (flagset.has("Omode:fiends")) {
                total_mandatory_bosses += 6;
                total_objective_count += 6;
            }
            if (flagset.has("Omode:classicforge")) {
                total_mandatory_tough_quests += 1;
                total_objective_count += 1;
            }
            if (flagset.has("Omode:classicgiant")) {
                total_mandatory_tough_quests += 1;
                total_objective_count += 1;
            }
            if ((flagset.get_list("^Omode:dkmatter").length > 0)) {
                total_objective_count += 1;
            }
            if ((flagset.get_list("^Omode:ki").length > 0)) {
                total_objective_count += 1;
            }
            if ((flagset.get_list("^Omode:goldhunter").length > 0)) {
                total_objective_count += 1;
            }
            if (flagset.has("Omode:external")) {
                total_objective_count += 1;
            }
            if (flagset.has("Kvanilla")) {
                if ((! _pj.in_es6("quest_tradepink", specific_tough_quest_objectives))) {
                    max_tough_quests -= 1;
                } else {
                    this._lib.push(log, ["error", "The objective-required Pink Tail is not available with vanilla key item placement"]);
                }
            } else {
                if (((((! flagset.has_any("Ksummon", "Kmoon", "Kforge", "Kpink", "Kmiab:standard", "Kmiab:above", "Kmiab:below", "Kmiab:lst", "Kmiab:all")) && flagset.has("Pkey")) && (! flagset.has("Owin:crystal"))) && flagset.has("Kstart:zonk"))) {
                    if ((! _pj.in_es6("quest_tradepink", specific_tough_quest_objectives))) {
                        max_tough_quests -= 1;
                    } else {
                        this._lib.push(log, ["error", "Both non-essential key items are removed on these flags, so the objective-required Pink Tail is not available"]);
                    }
                }
            }
            if (flagset.has("Bvanilla")) {
                for (var fl, _pj_c = 0, _pj_a = specific_boss_objectives, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                    fl = _pj_a[_pj_c];
                    current_boss = this._lib.re_sub("^O\\d+:boss_", "", fl);
                    if ((current_boss === "waterhag")) {
                        this._lib.push(log, ["error", `Objective boss specified (${current_boss}) when that boss is not in the vanilla boss assignment`]);
                    } else {
                        if ((((current_boss === "kingqueen") && flagset.has("Bremove:kqe_slot")) || ((current_boss === "officer") && flagset.has("Bremove:kaipo_slot")))) {
                            this._lib.push(log, ["error", `Objective specified for a boss removed from the vanilla boss assignment by Bremove: (${current_boss})`]);
                        }
                    }
                }
            }
            group_scores = [];
            for (var rand_pref, _pj_c = 0, _pj_a = ["Orandom:", "Orandom2:", "Orandom3:"], _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                rand_pref = _pj_a[_pj_c];
                rand_only_char_flags = flagset.get_list(`${rand_pref}only`);
                if ((rand_only_char_flags.length > 0)) {
                    for (var fl, _pj_f = 0, _pj_d = rand_only_char_flags, _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                        fl = _pj_d[_pj_f];
                        ch = this._lib.re_sub(`${rand_pref}only`, "", fl);
                        if ((! _pj.in_es6(ch, flags_objective_chars))) {
                            flagset.unset(fl);
                            this._lib.push(log, ["correction", `Random character objective restrictions set for characters guaranteed not to appear in the seed; removing ${fl}`]);
                        } else {
                            if (_pj.in_es6(ch, required_chars)) {
                                flagset.unset(fl);
                                this._lib.push(log, ["correction", `Random character objective restrictions set for characters with custom objectives set; removing ${fl}`]);
                            }
                        }
                    }
                }
                if (((! flagset.has(`${rand_pref}char`)) && (rand_only_char_flags.length > 0))) {
                    flagset.set(`${rand_pref}char`);
                    this._lib.push(log, ["correction", `Random objectives requiring specific characters set without Orandom:char; setting ${rand_pref}char`]);
                }
                all_customized_rand_flags = flagset.get_list((`^${rand_pref}` + "[^\\d]"));
                num_rand_objectives = flagset.get_list((`^${rand_pref}` + "[\\d]"));
                if ((num_rand_objectives.length === 0)) {
                    this._lib.push(group_scores, 0);
                    continue;
                }
                grp_obj_num = Number.parseInt(this._lib.re_sub(`^${rand_pref}`, "", num_rand_objectives[0]));
                rand_category_flags = [];
                for (var fl, _pj_f = 0, _pj_d = all_customized_rand_flags, _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                    fl = _pj_d[_pj_f];
                    if ((! _pj.in_es6(fl, rand_only_char_flags))) {
                        this._lib.push(rand_category_flags, fl);
                    }
                }
                if (((rand_category_flags.length === 0) || _pj.in_es6(`${rand_pref}boss`, rand_category_flags))) {
                    this._lib.push(group_scores, 100);
                    continue;
                }
                grp_sc = 0;
                if (_pj.in_es6(`${rand_pref}char`, rand_category_flags)) {
                    if (((rand_only_char_flags.length > 0) && (rand_only_char_flags.length < flags_objective_chars_num))) {
                        grp_sc += rand_only_char_flags.length;
                    } else {
                        grp_sc += flags_objective_chars_num;
                    }
                }
                if (_pj.in_es6(`${rand_pref}tough_quest`, rand_category_flags)) {
                    grp_sc += max_tough_quests;
                } else {
                    if (_pj.in_es6(`${rand_pref}quest`, rand_category_flags)) {
                        grp_sc += ((max_tough_quests + max_non_tough_quests) + 20);
                    }
                }
                grp_sc += (grp_obj_num - 4);
                this._lib.push(group_scores, grp_sc);
            }
            if ((group_scores[0] <= group_scores[1])) {
                if ((group_scores[2] < group_scores[0])) {
                    sorted_groups = ["Orandom3:", "Orandom:", "Orandom2:"];
                } else {
                    if ((group_scores[2] >= group_scores[1])) {
                        sorted_groups = ["Orandom:", "Orandom2:", "Orandom3:"];
                    } else {
                        sorted_groups = ["Orandom:", "Orandom3:", "Orandom2:"];
                    }
                }
            } else {
                if ((group_scores[2] < group_scores[1])) {
                    sorted_groups = ["Orandom3:", "Orandom2:", "Orandom:"];
                } else {
                    if ((group_scores[2] >= group_scores[0])) {
                        sorted_groups = ["Orandom2:", "Orandom:", "Orandom3:"];
                    } else {
                        sorted_groups = ["Orandom2:", "Orandom3:", "Orandom:"];
                    }
                }
            }
            for (var random_prefix, _pj_c = 0, _pj_a = sorted_groups, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                random_prefix = _pj_a[_pj_c];
                if ((flagset.get_list(`^${random_prefix}`).length === 0)) {
                    continue;
                }
                random_only_char_flags = flagset.get_list(`${random_prefix}only`);
                all_customized_random_flags = flagset.get_list((`^${random_prefix}` + "[^\\d]"));
                num_random_objectives = flagset.get_list((`^${random_prefix}` + "[\\d]"));
                if ((num_random_objectives.length === 0)) {
                    continue;
                }
                group_obj_num = Number.parseInt(this._lib.re_sub(`^${random_prefix}`, "", num_random_objectives[0]));
                total_objective_count += group_obj_num;
                random_category_flags = [];
                for (var fl, _pj_f = 0, _pj_d = all_customized_random_flags, _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                    fl = _pj_d[_pj_f];
                    if ((! _pj.in_es6(fl, random_only_char_flags))) {
                        this._lib.push(random_category_flags, fl);
                    }
                }
                bosses_available = false;
                if ((_pj.in_es6(`${random_prefix}boss`, random_category_flags) || (random_category_flags.length === 0))) {
                    bosses_available = true;
                }
                only_chars_list = [];
                for (var fl, _pj_f = 0, _pj_d = random_only_char_flags, _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                    fl = _pj_d[_pj_f];
                    this._lib.push(only_chars_list, fl.slice(`${random_prefix}only`.length));
                }
                just_in_case_mandatory_char_pool = [];
                only_char_objectives = false;
                if ((_pj.in_es6(`${random_prefix}char`, random_category_flags) && (random_category_flags.length === 1))) {
                    only_char_objectives = true;
                }
                theoretical_available_characters = 0;
                actual_available_characters = 0;
                duplicate_char_count = 0;
                if (_pj.in_es6(`${random_prefix}char`, random_category_flags)) {
                    if ((((random_only_char_flags.length > 0) && (random_only_char_flags.length < group_obj_num)) && (only_char_objectives === true))) {
                        this._lib.push(log, ["error", `Random objectives requiring fewer specific characters (${random_only_char_flags.length}) than number of objectives (${group_obj_num})`]);
                        break;
                    } else {
                        if (((flags_objective_chars_num < group_obj_num) && (only_char_objectives === true))) {
                            this._lib.push(log, ["error", `Fewer characters available (${flags_objective_chars_num}) than required number of random character objectives (${group_obj_num})`]);
                            break;
                        } else {
                            if ((random_only_char_flags.length > 0)) {
                                ch_list = only_chars_list;
                                ch_count_cap = random_only_char_flags.length;
                            } else {
                                ch_list = flags_objective_chars;
                                ch_count_cap = flags_objective_chars_num;
                            }
                            for (var current_char, _pj_f = 0, _pj_d = ch_list, _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                                current_char = _pj_d[_pj_f];
                                theoretical_available_characters += 1;
                                if (_pj.in_es6(current_char, character_pool)) {
                                    duplicate_char_count += 1;
                                } else {
                                    if ((only_char_objectives && (ch_count_cap === group_obj_num))) {
                                        this._lib.push(character_pool, current_char);
                                        this._lib.remove(flexible_char_pool, current_char);
                                    } else {
                                        this._lib.push(just_in_case_mandatory_char_pool, current_char);
                                        if ((! _pj.in_es6(current_char, flexible_char_pool))) {
                                            this._lib.push(flexible_char_pool, current_char);
                                        }
                                    }
                                }
                            }
                        }
                    }
                    if ((theoretical_available_characters > flags_objective_chars_num)) {
                        theoretical_available_characters = flags_objective_chars_num;
                    }
                    if (((total_char_count > duplicate_char_count) && (random_only_char_flags.length === 0))) {
                        duplicate_char_count = total_char_count;
                    }
                    actual_available_characters = (theoretical_available_characters - duplicate_char_count);
                    if (((actual_available_characters < group_obj_num) && (only_char_objectives === true))) {
                        this._lib.push(log, ["error", `Not enough unique characters for pool ${random_prefix}. Other pools and custom objectives have consumed too many characters by now`]);
                        break;
                    }
                }
                min_non_char_objectives = 0;
                if ((actual_available_characters < group_obj_num)) {
                    min_non_char_objectives = (group_obj_num - actual_available_characters);
                }
                max_char_objectives = actual_available_characters;
                while ((max_char_objectives > group_obj_num)) {
                    max_char_objectives -= 1;
                }
                if (bosses_available) {
                    if ((random_category_flags.length === 1)) {
                        total_mandatory_bosses += group_obj_num;
                    } else {
                        if (((random_category_flags.length === 2) && _pj.in_es6(`${random_prefix}char`, random_category_flags))) {
                            total_mandatory_bosses += min_non_char_objectives;
                            total_flexible_bosses += (group_obj_num - min_non_char_objectives);
                            flexible_char_count += max_char_objectives;
                            flexible_random_objective_count += (group_obj_num - min_non_char_objectives);
                        } else {
                            if (((random_category_flags.length === 2) && (! _pj.in_es6(`${random_prefix}char`, random_category_flags)))) {
                                if (_pj.in_es6(`${random_prefix}quest`, random_category_flags)) {
                                    non_tough_quest_room = ((max_non_tough_quests - total_mandatory_non_tough_quests) - total_flexible_non_tough_quests);
                                    tough_quest_room = ((max_tough_quests - total_mandatory_tough_quests) - total_flexible_tough_quests);
                                    if (((non_tough_quest_room < group_obj_num) && (tough_quest_room >= group_obj_num))) {
                                        total_flexible_non_tough_quests += non_tough_quest_room;
                                        total_flexible_tough_quests += group_obj_num;
                                        total_flexible_bosses += group_obj_num;
                                        flexible_random_objective_count += group_obj_num;
                                    } else {
                                        if (((non_tough_quest_room >= group_obj_num) && (tough_quest_room < group_obj_num))) {
                                            total_flexible_non_tough_quests += group_obj_num;
                                            total_flexible_tough_quests += tough_quest_room;
                                            total_flexible_bosses += group_obj_num;
                                            flexible_random_objective_count += group_obj_num;
                                        } else {
                                            if (((non_tough_quest_room < group_obj_num) && (tough_quest_room < group_obj_num))) {
                                                total_flexible_non_tough_quests += non_tough_quest_room;
                                                total_flexible_tough_quests += tough_quest_room;
                                                if (((non_tough_quest_room + tough_quest_room) < group_obj_num)) {
                                                    total_mandatory_bosses += ((group_obj_num - non_tough_quest_room) - tough_quest_room);
                                                    total_flexible_bosses += (non_tough_quest_room + tough_quest_room);
                                                    flexible_random_objective_count += (non_tough_quest_room + tough_quest_room);
                                                } else {
                                                    total_flexible_bosses += group_obj_num;
                                                    flexible_random_objective_count += group_obj_num;
                                                }
                                            } else {
                                                total_flexible_non_tough_quests += group_obj_num;
                                                total_flexible_tough_quests += group_obj_num;
                                                total_flexible_bosses += group_obj_num;
                                                flexible_random_objective_count += group_obj_num;
                                            }
                                        }
                                    }
                                } else {
                                    if (_pj.in_es6(`${random_prefix}tough_quest`, random_category_flags)) {
                                        tough_quest_room = ((max_tough_quests - total_mandatory_tough_quests) - total_flexible_tough_quests);
                                        if ((tough_quest_room < group_obj_num)) {
                                            total_flexible_tough_quests += tough_quest_room;
                                            total_mandatory_bosses += (group_obj_num - tough_quest_room);
                                            total_flexible_bosses += tough_quest_room;
                                            flexible_random_objective_count += tough_quest_room;
                                        } else {
                                            total_flexible_tough_quests += group_obj_num;
                                            total_flexible_bosses += group_obj_num;
                                            flexible_random_objective_count += group_obj_num;
                                        }
                                    }
                                }
                            } else {
                                if (((random_category_flags.length === 3) && _pj.in_es6(`${random_prefix}tough_quest`, random_category_flags))) {
                                    tough_quest_room = ((max_tough_quests - total_mandatory_tough_quests) - total_flexible_tough_quests);
                                    if (((tough_quest_room < group_obj_num) && (min_non_char_objectives === 0))) {
                                        total_flexible_tough_quests += tough_quest_room;
                                        flexible_char_count += max_char_objectives;
                                        total_flexible_bosses += group_obj_num;
                                        flexible_random_objective_count += group_obj_num;
                                    } else {
                                        if (((tough_quest_room < group_obj_num) && (min_non_char_objectives > 0))) {
                                            total_flexible_tough_quests += tough_quest_room;
                                            flexible_char_count += max_char_objectives;
                                            if (((tough_quest_room + max_char_objectives) < group_obj_num)) {
                                                total_mandatory_bosses += ((group_obj_num - tough_quest_room) - max_char_objectives);
                                                total_flexible_bosses += (tough_quest_room + max_char_objectives);
                                                flexible_random_objective_count += (tough_quest_room + max_char_objectives);
                                            } else {
                                                total_flexible_bosses += group_obj_num;
                                                flexible_random_objective_count += group_obj_num;
                                            }
                                        } else {
                                            flexible_char_count += max_char_objectives;
                                            total_flexible_tough_quests += group_obj_num;
                                            total_flexible_bosses += group_obj_num;
                                            flexible_random_objective_count += group_obj_num;
                                        }
                                    }
                                } else {
                                    non_tough_quest_room = ((max_non_tough_quests - total_mandatory_non_tough_quests) - total_flexible_non_tough_quests);
                                    tough_quest_room = ((max_tough_quests - total_mandatory_tough_quests) - total_flexible_tough_quests);
                                    if ((non_tough_quest_room < group_obj_num)) {
                                        total_flexible_non_tough_quests += non_tough_quest_room;
                                    } else {
                                        total_flexible_non_tough_quests += group_obj_num;
                                    }
                                    if ((tough_quest_room < group_obj_num)) {
                                        total_flexible_non_tough_quests += tough_quest_room;
                                    } else {
                                        total_flexible_tough_quests += group_obj_num;
                                    }
                                    flexible_char_count += max_char_objectives;
                                    total_flexible_bosses += group_obj_num;
                                    flexible_random_objective_count += group_obj_num;
                                }
                            }
                        }
                    }
                } else {
                    if ((random_category_flags.length === 1)) {
                        if (_pj.in_es6(`${random_prefix}char`, random_category_flags)) {
                            total_char_count += group_obj_num;
                        } else {
                            if (_pj.in_es6(`${random_prefix}quest`, random_category_flags)) {
                                non_tough_quest_room = ((max_non_tough_quests - total_mandatory_non_tough_quests) - total_flexible_non_tough_quests);
                                tough_quest_room = ((max_tough_quests - total_mandatory_tough_quests) - total_flexible_tough_quests);
                                if (((non_tough_quest_room + tough_quest_room) < group_obj_num)) {
                                    this._lib.push(log, ["error", `Too many quests (tough and non-tough) have been consumed by now (${random_prefix}), between custom objectives and other pools`]);
                                    break;
                                }
                                if (((non_tough_quest_room < group_obj_num) && (tough_quest_room >= group_obj_num))) {
                                    total_flexible_non_tough_quests += non_tough_quest_room;
                                    total_mandatory_tough_quests += (group_obj_num - non_tough_quest_room);
                                    total_flexible_tough_quests += non_tough_quest_room;
                                    flexible_random_objective_count += non_tough_quest_room;
                                } else {
                                    if (((non_tough_quest_room >= group_obj_num) && (tough_quest_room < group_obj_num))) {
                                        total_flexible_tough_quests += tough_quest_room;
                                        total_mandatory_non_tough_quests += (group_obj_num - tough_quest_room);
                                        total_flexible_non_tough_quests += tough_quest_room;
                                        flexible_random_objective_count += tough_quest_room;
                                    } else {
                                        if (((non_tough_quest_room < group_obj_num) && (tough_quest_room < group_obj_num))) {
                                            total_mandatory_non_tough_quests += (group_obj_num - tough_quest_room);
                                            total_flexible_non_tough_quests += (non_tough_quest_room - (group_obj_num - tough_quest_room));
                                            total_mandatory_tough_quests += (group_obj_num - non_tough_quest_room);
                                            total_flexible_tough_quests += (tough_quest_room - (group_obj_num - non_tough_quest_room));
                                            flexible_random_objective_count += ((non_tough_quest_room + tough_quest_room) - group_obj_num);
                                        } else {
                                            total_flexible_non_tough_quests += group_obj_num;
                                            total_flexible_tough_quests += group_obj_num;
                                            flexible_random_objective_count += group_obj_num;
                                        }
                                    }
                                }
                            } else {
                                tough_quest_room = ((max_tough_quests - total_mandatory_tough_quests) - total_flexible_tough_quests);
                                if ((tough_quest_room < group_obj_num)) {
                                    if (((tough_quest_room + total_flexible_tough_quests) < group_obj_num)) {
                                        this._lib.push(log, ["error", `Too many tough quests have been consumed by now (${random_prefix}), between custom objectives and other pools`]);
                                        break;
                                    } else {
                                        total_mandatory_tough_quests += tough_quest_room;
                                        total_flexible_tough_quests -= (group_obj_num - tough_quest_room);
                                    }
                                } else {
                                    total_mandatory_tough_quests += group_obj_num;
                                }
                            }
                        }
                    } else {
                        if (_pj.in_es6(`${random_prefix}tough_quest`, random_category_flags)) {
                            tough_quest_room = ((max_tough_quests - total_mandatory_tough_quests) - total_flexible_tough_quests);
                            if (((tough_quest_room + max_char_objectives) < group_obj_num)) {
                                if ((((tough_quest_room + max_char_objectives) + total_flexible_tough_quests) < group_obj_num)) {
                                    this._lib.push(log, ["error", `Too many tough quests and characters have been consumed by now (${random_prefix}), between custom objectives and other pools`]);
                                    break;
                                } else {
                                    total_mandatory_tough_quests += tough_quest_room;
                                    total_flexible_tough_quests -= ((group_obj_num - tough_quest_room) - max_char_objectives);
                                    total_char_count += max_char_objectives;
                                }
                            } else {
                                if ((tough_quest_room < min_non_char_objectives)) {
                                    if (((tough_quest_room + total_flexible_tough_quests) < min_non_char_objectives)) {
                                        this._lib.push(log, ["error", `Too many tough quest objectives are required for the number of character objectives that are left (${random_prefix})`]);
                                        break;
                                    } else {
                                        total_mandatory_tough_quests += tough_quest_room;
                                        total_flexible_tough_quests -= (min_non_char_objectives - tough_quest_room);
                                        total_char_count += max_char_objectives;
                                    }
                                } else {
                                    if ((min_non_char_objectives === 0)) {
                                        if ((tough_quest_room < group_obj_num)) {
                                            total_char_count += (group_obj_num - tough_quest_room);
                                            flexible_char_count += tough_quest_room;
                                            total_flexible_tough_quests += tough_quest_room;
                                            if ((actual_available_characters === group_obj_num)) {
                                                for (var ch, _pj_f = 0, _pj_d = just_in_case_mandatory_char_pool, _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                                                    ch = _pj_d[_pj_f];
                                                    this._lib.push(character_pool, ch);
                                                    this._lib.remove(flexible_char_pool, ch);
                                                }
                                            } else {
                                                flexible_random_objective_count += tough_quest_room;
                                            }
                                        } else {
                                            flexible_char_count += group_obj_num;
                                            total_flexible_tough_quests += group_obj_num;
                                            flexible_random_objective_count += group_obj_num;
                                        }
                                    } else {
                                        if ((tough_quest_room < group_obj_num)) {
                                            if (((tough_quest_room + total_flexible_tough_quests) < group_obj_num)) {
                                                total_char_count += (group_obj_num - (tough_quest_room + total_flexible_tough_quests));
                                                flexible_char_count += (max_char_objectives - ((group_obj_num - tough_quest_room) - total_flexible_tough_quests));
                                                total_mandatory_tough_quests += min_non_char_objectives;
                                                flexible_random_objective_count += ((tough_quest_room + total_flexible_tough_quests) - min_non_char_objectives);
                                                total_flexible_tough_quests += (tough_quest_room - min_non_char_objectives);
                                            } else {
                                                if ((tough_quest_room < min_non_char_objectives)) {
                                                    total_mandatory_tough_quests += tough_quest_room;
                                                    total_flexible_tough_quests += ((group_obj_num - min_non_char_objectives) - (min_non_char_objectives - tough_quest_room));
                                                    flexible_char_count += max_char_objectives;
                                                    flexible_random_objective_count += (group_obj_num - min_non_char_objectives);
                                                } else {
                                                    total_mandatory_tough_quests += min_non_char_objectives;
                                                    total_flexible_tough_quests += (group_obj_num - min_non_char_objectives);
                                                    flexible_char_count += max_char_objectives;
                                                    flexible_random_objective_count += (group_obj_num - min_non_char_objectives);
                                                }
                                            }
                                        } else {
                                            total_mandatory_tough_quests += min_non_char_objectives;
                                            total_flexible_tough_quests += (group_obj_num - min_non_char_objectives);
                                            flexible_char_count += max_char_objectives;
                                            flexible_random_objective_count += (group_obj_num - min_non_char_objectives);
                                        }
                                    }
                                }
                            }
                        } else {
                            non_tough_quest_room = ((max_non_tough_quests - total_mandatory_non_tough_quests) - total_flexible_non_tough_quests);
                            tough_quest_room = ((max_tough_quests - total_mandatory_tough_quests) - total_flexible_tough_quests);
                            if ((min_non_char_objectives === 0)) {
                                flexible_char_count += group_obj_num;
                                flexible_random_objective_count += group_obj_num;
                                if ((non_tough_quest_room < group_obj_num)) {
                                    total_flexible_non_tough_quests += non_tough_quest_room;
                                } else {
                                    total_flexible_non_tough_quests += group_obj_num;
                                }
                                if ((tough_quest_room < group_obj_num)) {
                                    total_flexible_tough_quests += tough_quest_room;
                                } else {
                                    total_flexible_tough_quests += group_obj_num;
                                }
                            } else {
                                flexible_char_count += (group_obj_num - min_non_char_objectives);
                                flexible_random_objective_count += group_obj_num;
                                if ((non_tough_quest_room < group_obj_num)) {
                                    total_flexible_non_tough_quests += non_tough_quest_room;
                                    total_flexible_tough_quests += group_obj_num;
                                } else {
                                    if ((tough_quest_room < group_obj_num)) {
                                        total_flexible_non_tough_quests += group_obj_num;
                                        total_flexible_tough_quests += tough_quest_room;
                                    } else {
                                        total_flexible_non_tough_quests += group_obj_num;
                                        total_flexible_tough_quests += group_obj_num;
                                    }
                                }
                            }
                        }
                    }
                }
            }
            max_bosses = 34;
            boss_slots_removed = 0;
            removed_bosses_flags = flagset.get_list(`^Bremove:`);
            for (var slot, _pj_c = 0, _pj_a = removed_bosses_flags, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                slot = _pj_a[_pj_c];
                max_bosses -= 1;
                boss_slots_removed += 1;
            }
            if ((total_mandatory_bosses > max_bosses)) {
                this._lib.push(log, ["error", `${total_mandatory_bosses} guaranteed boss objectives specified with only ${max_bosses} bosses available (${boss_slots_removed} bosses removed)`]);
            }
            if ((total_mandatory_tough_quests > max_tough_quests)) {
                this._lib.push(log, ["error", `${total_mandatory_tough_quests} guaranteed tough quest objectives specified with only ${max_tough_quests} tough quests available`]);
            }
            if ((total_objective_count > 32)) {
                this._lib.push(log, ["error", "More than 32 objectives specified"]);
            }
            if ((total_char_count > nonstarting_character_slots)) {
                this._lib.push(log, ["error", `Not enough available non-starting character slots for all of the mandatory character objectives specified (between fixed objectives and random pools). Either add more character slots back in, remove character objectives, or allow other objective types for some random pools.`]);
            } else {
                if (flagset.has("Cvanilla")) {
                    available_vanilla_chars = 11;
                    if ((flagset.has("Cnofree") && (! flagset.has("Ctreasure:free")))) {
                        available_vanilla_chars -= 4;
                    }
                    if ((flagset.has("Cnoearned") && (! flagset.has("Ctreasure:earned")))) {
                        available_vanilla_chars -= 7;
                    }
                    if ((total_char_count > available_vanilla_chars)) {
                        this._lib.push(log, ["error", `Not enough available non-starting vanilla characters for all of the mandatory character objectives specified (between fixed objectives and random pools). Either add more character slots back in, remove character objectives, or allow other objective types for some random pools.`]);
                    }
                } else {
                    distinct_flags = flagset.get_list("^Cdistinct:");
                    if ((distinct_flags.length > 0)) {
                        distinct_count = Number.parseInt(this._lib.re_sub("^Cdistinct:", "", distinct_flags[0]));
                        if ((total_char_count > distinct_count)) {
                            this._lib.push(log, ["error", `Too few distinct characters specified for the mandatory character objectives. Either increase the number of distinct characters, or remove character objectives.`]);
                        }
                    }
                }
            }
            while (((total_mandatory_tough_quests + total_flexible_tough_quests) > max_tough_quests)) {
                total_flexible_tough_quests -= 1;
            }
            while (((total_mandatory_non_tough_quests + total_flexible_non_tough_quests) > max_non_tough_quests)) {
                total_flexible_non_tough_quests -= 1;
            }
            while (((total_mandatory_bosses + total_flexible_bosses) > max_bosses)) {
                total_flexible_bosses -= 1;
            }
            if (((((flexible_char_count + total_flexible_bosses) + total_flexible_non_tough_quests) + total_flexible_tough_quests) < flexible_random_objective_count)) {
                this._lib.push(log, ["error", `There are too many restrictions on the types of random objectives to select enough random objectives satisfying the flags.`]);
            }
        }
        challenges = flagset.get_list("^-wacky:");
        if (challenges) {
            WACKY_SET_1 = ["afflicted", "menarepigs", "mirrormirror", "skywarriors", "zombies"];
            WACKY_SET_2 = ["battlescars", "payablegolbez", "tellahmaneuver", "worthfighting"];
            WACKY_SET_3 = [["3point", "afflicted", "battlescars", "menarepigs", "mirrormirror", "skywarriors", "unstackable", "zombies"], ["afflicted", "friendlyfire"], ["battlescars", "afflicted", "zombies", "worthfighting"], ["darts", "musical", "skillissue"], ["3point", "tellahmaneuver"]];
            for (var c, _pj_c = 0, _pj_a = challenges, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
                c = _pj_a[_pj_c];
                mode = this._lib.re_sub("-wacky:", "", c);
                if (_pj.in_es6(mode, WACKY_SET_1)) {
                    this._simple_disable(flagset, log, "Can only have one enforced status wacky mode", function () {
    var _pj_d = [], _pj_e = WACKY_SET_1;
    for (var _pj_f = 0, _pj_g = _pj_e.length; (_pj_f < _pj_g); _pj_f += 1) {
        var m = _pj_e[_pj_f];
        if ((m !== mode)) {
            _pj_d.push(`-wacky:${m}`);
        }
    }
    return _pj_d;
}
.call(this));
                    this._simple_disable(flagset, log, "Modes are incompatible with enforced status wacky modes", function () {
    var _pj_d = [], _pj_e = WACKY_SET_2;
    for (var _pj_f = 0, _pj_g = _pj_e.length; (_pj_f < _pj_g); _pj_f += 1) {
        var m = _pj_e[_pj_f];
        _pj_d.push(`-wacky:${m}`);
    }
    return _pj_d;
}
.call(this));
                }
                for (var group, _pj_f = 0, _pj_d = WACKY_SET_3, _pj_e = _pj_d.length; (_pj_f < _pj_e); _pj_f += 1) {
                    group = _pj_d[_pj_f];
                    if (_pj.in_es6(mode, group)) {
                        this._simple_disable(flagset, log, `Wacky modes are incompatible with ${mode}`, function () {
    var _pj_g = [], _pj_h = group;
    for (var _pj_i = 0, _pj_j = _pj_h.length; (_pj_i < _pj_j); _pj_i += 1) {
        var m = _pj_h[_pj_i];
        if ((m !== mode)) {
            _pj_g.push(`-wacky:${m}`);
        }
    }
    return _pj_g;
}
.call(this));
                    }
                }
            }
        }
        return log;
    }
}

//# sourceMappingURL=flagsetcore.js.map
