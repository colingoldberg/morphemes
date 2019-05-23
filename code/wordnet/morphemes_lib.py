# morphemes_lib.py

import json
import copy
import morphemes_wn as mdb

data_directory_path = "../../data/"

debug = 0

examples = []

vowels = ["a", "e", "i", "o", "u"]
vowels_plus_y = ["a", "e", "i", "o", "u", "y"]
consonants = ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"]

def find_prefixes_for_word_segment(word_array):
	ret_prefixes = {}
	if len(word_array) > 0:
		word = word_array[0]
		for rxk in morphemes:
			rx = morphemes[rxk]
			for form_obj in rx["forms"]:
				if form_obj["loc"] == "prefix":
					fform = form_obj["form"]
					if word.startswith(fform):
						ret_prefix = {
							"loc": "prefix",
							"root": rx,
							"form": fform,
							"len": len(fform),
							"meaning": rx["meaning"]
						}
						if "category" in form_obj:
							ret_prefix["category"] = form_obj["category"]
						#rpk = rxk + "-" + fform ??
						ret_prefixes[rxk] = ret_prefix
						break
	else:
		if debug > 0:
			print("find_prefixes_for_word_segment: empty word_array")
	return ret_prefixes

def find_suffixes_for_word_segment(word_array):
	ret_suffixes = {}
	if len(word_array) > 0:
		word = word_array[len(word_array)-1]
		for rxk in morphemes:
			rx = morphemes[rxk]
			for form_obj in rx["forms"]:
				if form_obj["loc"] == "suffix":
					fform = form_obj["form"]
					if word.endswith(fform):
						ret_suffix = {
							"loc": "suffix",
							"root": rx,
							"form": fform,
							"len": len(fform),
							"meaning": rx["meaning"]
						}
						rsk = rxk + "-" + fform
						ret_suffixes[rsk] = ret_suffix
						#break
	else:
		if debug > 0:
			print("find_suffixes_for_word_segment: empty word_array")
	return ret_suffixes

def find_roots_for_word_segment(word_array):
	"roots, stems coded as embedded"
	ret_roots = {}
	if len(word_array) > 0:
		if len(word_array) > 1:
			word = word_array[0]
			if debug > 0:
				print("find_roots_for_word_segment: len word_array > 1: ", word_array)
		else:
			word = word_array[0]
		for rxk in morphemes:
			rx = morphemes[rxk]
			for form_obj in rx["forms"]:
				if form_obj["loc"] == "embedded":
					fform = form_obj["form"]
					if fform in word:
						ret_root = {
							"loc": "embedded",
							"root": rx,
							"form": fform,
							"len": len(fform),
							"meaning": rx["meaning"]
						}
						ret_roots[rxk] = ret_root
						break
	else:
		if debug > 0:
			print("find_roots_for_word_segment: empty word_array")
	return ret_roots

def get_prefix_exact_match(found_prefixes, mf_prefix):
	for pfxk in found_prefixes:
		pfx = found_prefixes[pfxk]
		pforms = pfx["root"]["forms"]
		for pform in pforms:
			if pform["form"] == mf_prefix:
				return pfxk, pfx
	return None, None

def get_suffix_exact_match(found_suffixes, mf_suffix):
	for sfxk in found_suffixes:
		sfx = found_suffixes[sfxk]
		sforms = sfx["root"]["forms"]
		for sform in sforms:
			if sform["form"] == mf_suffix:
				return sfxk, sfx
	return None, None

def find_best_entry(strategy_leg, entries, form_array, strategy):
	"best affix from affixes found, depending on strategy"
	all_entries = entries.copy()
	best_entry = {
		"key": "",
		"form": "",
		"len": 0,
		"meaning": []
	}
	if len(form_array) > 0:
		form = form_array[0]
		if len(form_array) > 1:
			if debug > 0:
				print("find_best_entry: form_array len > 1")
		form_len = len(form)
		best_ix = form_len - 1
		if len(entries) > 0:
			for entryx in entries:
				entry = entries[entryx]
				if strategy == "max_len":
					if entry["len"] > best_entry["len"] and entry["len"] <= form_len:
						best_entry["key"] = entryx
						best_entry["form"] = entry["form"]
						best_entry["len"] = entry["len"]
						best_entry["meaning"] = entry["meaning"]
				elif strategy == "left_first":
					entry_form_ix = form.index(entry["form"])
					if entry_form_ix < best_ix and entry["len"] <= form_len:
						best_entry["key"] = entryx
						best_entry["form"] = entry["form"]
						best_entry["len"] = entry["len"]
						best_entry["meaning"] = entry["meaning"]
						best_ix = entry_form_ix
			all_entries[best_entry["key"]]["priority"] = "highest"
			return best_entry, all_entries[best_entry["key"]], all_entries
		else:
			return {}, {}, all_entries
	else:
		if debug > 0:
			print("find_best_entry: empty form_array")
		return {}, {}, all_entries

def find_max_entry(strategy_leg, entries, form_array):
	"best affix from affixes , based on length"
	all_entries = entries.copy()
	max_entry = {
		"key": "",
		"form": "",
		"len": 0,
		"meaning": []
	}
	if len(form_array) > 0:
		if strategy_leg == "prefix":
			form = form_array[0]
		elif strategy_leg == "suffix":
			form = form_array[len(form_array)-1]
		if len(form_array) > 1:
			if debug > 0:
				print("find_max_entry: form_array len > 1")
		form_len = len(form)
		if len(entries) > 0:
			for entryx in entries:
				entry = entries[entryx]
				if entry["len"] > max_entry["len"] and entry["len"] <= form_len:
					max_entry["key"] = entryx
					max_entry["form"] = entry["form"]
					max_entry["len"] = entry["len"]
					max_entry["meaning"] = entry["meaning"]
			if max_entry["key"] != "":
				all_entries[max_entry["key"]]["priority"] = "highest"
				return max_entry, all_entries[max_entry["key"]], all_entries
			else:
				return {}, {}, all_entries
		else:
			return {}, {}, all_entries
	else:
		if debug > 0:
			print("find_max_entry: empty form_array")
		return {}, {}, all_entries

def unique_keys(list1):
	list_set = set(list1)
	unique_list = (list(list_set))
	return unique_list

def save_result(leg, xk_entry, x, prior_results, all_entries):
	"add to results object"
	ret_results = prior_results
	wcp_update = []
	leg_obj = {
		"leg": leg,
		"xk": xk_entry["key"],
		"form": xk_entry["form"],
		"meaning": xk_entry["meaning"],
		"x": x,
		"all_entries": all_entries
	}
	if leg == "prefix" and "category" in x:
		leg_obj["category"] = x["category"]
	if leg in ret_results:
		ret_results[leg].append(leg_obj)
	else:
		ret_results[leg] = [leg_obj]

	for word_segment in ret_results["word_components_potential"]:
		if xk_entry["form"] in word_segment:
			if len(xk_entry["form"]) == len(word_segment):
				pass
			else:
				word_segment_array = word_segment.split(xk_entry["form"])
				for wsa_element in word_segment_array:
					if wsa_element != '':
						wcp_update.append(wsa_element)
		else:
			wcp_update.append(word_segment)
	ret_results["word_components_potential"] = wcp_update
	ret_results["matched_char_count"] += len(xk_entry["form"])
	ret_results["unmatched_char_count"] -= len(xk_entry["form"])
	return ret_results

# Based on the intersection of longest found prefixes, suffixes, roots
# ie. using length as score
# also subject to max length of form
# c/f Scrabble
def find_likely_entries(prior_results, strategy_tuple, root_strategy):
	ret_results = prior_results
	strategy = list(strategy_tuple)

	while len(strategy) > 0:
		strategy_leg = strategy.pop(0)
		if strategy_leg == "prefix":
			if len(ret_results["word_components_potential"]) > 0:
				find_prefixes = find_prefixes_for_word_segment(ret_results["word_components_potential"])
				max_entry, max_px, all_rx = find_max_entry(strategy_leg, find_prefixes, ret_results["word_components_potential"])
				#if max_entry["key"] != "":
				if len(max_entry) > 0:
					ret_results = save_result("prefix", max_entry, max_px, ret_results, all_rx)
		elif strategy_leg == "root":
			if len(ret_results["word_components_potential"]) > 0:
				find_roots = find_roots_for_word_segment(ret_results["word_components_potential"])
				best_entry, best_rx, all_rx = find_best_entry(strategy_leg, find_roots, ret_results["word_components_potential"], root_strategy)
				#if best_entry["key"] != "":
				if len(max_entry) > 0:
					ret_results = save_result("root", best_entry, best_rx, ret_results, all_rx)
		elif strategy_leg == "suffix":
			find_suffixes = find_suffixes_for_word_segment(ret_results["word_components_potential"])
			max_entry, max_sx, all_rx = find_max_entry(strategy_leg, find_suffixes, ret_results["word_components_potential"])
			#if max_entry["key"] != "":
			if len(max_entry) > 0:
				ret_results = save_result("suffix", max_entry, max_sx, ret_results, all_rx)
	return ret_results

def find_entry_in_db(word, strategy, root_strategy):
	"assumes no prior results"
	global debug

	results = {
		"word": word,
		"matched_char_count": 0,
		"unmatched_char_count": len(word),
		"word_components_potential": [word]
	}
	results = find_likely_entries(results, strategy, root_strategy)
	return results

def find_entry_in_db_multiple_strategies(word):
	"try up to four strategies"

	strategy = ("suffix", "root", "prefix")
	root_strategy = "max_len" # left_first | max_len

	results = find_entry_in_db(word, strategy, root_strategy)
	if debug > 0:
		print(results)
		print(format_results(results, "+"))

	#Check all characters accounted for, and in right order
	if results["unmatched_char_count"] > 0 or format_results(results, "") != word:
		strategy = ("suffix", "prefix", "root")
		results = find_entry_in_db(word, strategy, root_strategy)
		if debug > 0:
			print(results)
			print(format_results(results, "+"))

	if results["unmatched_char_count"] > 0 or format_results(results, "") != word:
		strategy = ("prefix", "root", "suffix")
		results = find_entry_in_db(word, strategy, root_strategy)
		if debug > 0:
			print(results)
			print(format_results(results, "+"))

	if results["unmatched_char_count"] > 0 or format_results(results, "") != word:
		strategy = ("prefix", "suffix", "root")
		results = find_entry_in_db(word, strategy, root_strategy)
		if debug > 0:
			print(results)
			print(format_results(results, "+"))
	return results

def apply_consonant_doubling(prior_results, loc):
	results = prior_results.copy()
	if "suffix" in results:
		if results["suffix"][0]["form"][0] in vowels_plus_y: # was just vowels
			if loc in results:
				cd_candidate = results[loc][0]["form"]
				cd_candidate_last_char = cd_candidate[len(cd_candidate)-1]
				if cd_candidate_last_char in consonants:
					results[loc][0]["form"] += cd_candidate_last_char
					results["unmatched_char_count"] = 0
					results["matched_char_count"] += 1
	return results

def discover_segments(word):
	"top-level function, used by client application"
	
	results = find_entry_in_db_multiple_strategies(word)

	if results["unmatched_char_count"] == 1:
		results = apply_consonant_doubling(results, "root")
	if results["unmatched_char_count"] == 1:
		results = apply_consonant_doubling(results, "prefix")

	temp_results = copy.deepcopy(results) #in case root, prefix are popped
	if results["unmatched_char_count"] > 0 or format_results(results, "") != word:
		results = mdb.find_entry_in_db_given_suffix(word, results)
	if results["unmatched_char_count"] > 0 or format_results(results, "") != word:
		results = copy.deepcopy(temp_results)
		results = mdb.find_entry_in_db_given_suffix_and_prefix(word, results)
	if results["unmatched_char_count"] > 0 or format_results(results, "") != word:
		results = copy.deepcopy(temp_results)
		results = mdb.find_entry_in_db_given_prefix(word, results)
	return results

def find_examples_for_morpheme(morpheme, loc):
	ret_words = []
	max_example_count = 10
	example_count = 0
	morpheme_len = len(morpheme)
	for example in examples:
		example_count += 1
		if example_count > max_example_count:
			break
		example_len = len(example)
		if example_len > morpheme_len:
			if loc == "prefix":
				if example.startswith(morpheme):
					ret_words.append(example)
			elif loc == "suffix":
				if example.endswith(morpheme):
					ret_words.append(example)
			elif loc == "root":
				within_example = example[1:][:example_len-2]
				if morpheme in within_example:
					ret_words.append(example)
	return ret_words

def format_results(results, delimiter):
	"Assume one each of prefix, root, suffix"
	prefix = ""
	suffix = ""
	embedded = ""
	if "prefix" in results and results["prefix"] != None and results["prefix"][0] != None:
		prefix = results["prefix"][0]["form"]
	if "root" in results and results["root"] != None and results["root"][0] != None:
		embedded = results["root"][0]["form"]
	if "suffix" in results and results["suffix"] != None and results["suffix"][0] != None:
		suffix = results["suffix"][0]["form"]
	return prefix + delimiter + embedded + delimiter + suffix

def generate_final_results(results):
	"Final result returned to client"
	ret_results = {
		"word": results["word"],
		"segments": format_results(results, "+"),
		"matched_char_count": results["matched_char_count"],
		"unmatched_char_count": results["unmatched_char_count"]
	}
	if "prefix" in results and results["prefix"] != None and results["prefix"][0] != None:
		prefix_result = {
			"form": results["prefix"][0]["form"],
			"meaning": get_results_meaning(results, "prefix")
		}
		ret_results["prefix"] = prefix_result
	if "root" in results and results["root"] != None and results["root"][0] != None:
		root_result = {
			"form": results["root"][0]["form"],
			"meaning": get_results_meaning(results, "root")
		}
		ret_results["root"] = root_result
	if "suffix" in results and results["suffix"] != None and results["suffix"][0] != None:
		suffix_result = {
			"form": results["suffix"][0]["form"],
			"meaning": get_results_meaning(results, "suffix")
		}
		ret_results["suffix"] = suffix_result
	return ret_results

def get_results_meaning(results, leg):
	if results[leg][0] != None:
		if "meaning" in results[leg][0]:
			return results[leg][0]["meaning"]
		elif "wn_result" in results[leg][0]:
			return results[leg][0]["wn_result"]["word_node"]
		else:
			return []
	else:
		return []

def close_neo4j():
	mdb.close_neo4j()

morphemes_filename = "morphemes.json"
morphemes_filepath = data_directory_path + morphemes_filename
morphemes_file = open(morphemes_filepath, "r")
morphemes = json.loads(morphemes_file.read())
