# morphemes_wn.py

from nltk.corpus import wordnet as wn
import morphemes_lib as morphemes

debug = 0


def find_entry_in_db_given_suffix(word, prior_results):
	results = prior_results
	if "suffix" in results:
		suffixes = results["suffix"][0]["all_entries"]
		for sfx in suffixes:
			suffix = suffixes[sfx]["form"]
			sw_len = len(word) - len(suffix)
			search_word = word[:sw_len]
			word_result = find_word_in_db(search_word)
			if word_result != None and word_result["word_node_id"] > 0:
				if debug > 0:
					print("found word in wn: ", search_word, word, word_result["word_node_id"])
				word_node = word_result["word_node"]
				if "prefix" in results:
					results["prefix"][0]["form"] = search_word
					results["prefix"][0]["db_form"] = word_node[0]["name"]
					results["prefix"][0]["wn_result"] = word_result
				else:
					result = {
						"form": search_word,
						"db_form": word_node[0]["name"],
						"wn_result": word_result
					}
					results["prefix"] = []
					results["prefix"].append(result)
				if "root" in results:
					#results["root"][0]["form"] = ""
					results["root"][0] = None
				results["suffix"][0]["form"] = suffix
				results["suffix"][0]["meaning"] = suffixes[sfx]["meaning"]
				if morphemes.format_results(results, "") == word:
					results["unmatched_char_count"] = 0
					break
	return results

def find_entry_in_db_given_prefix(word, prior_results):
	results = prior_results.copy()
	if "prefix" in results:
		prefixes = results["prefix"][0]["all_entries"]
		for pfx in prefixes:
			prefix = prefixes[pfx]["form"]
			search_word = word[len(prefix):]
			word_result = find_word_in_db(search_word)
			if word_result != None and word_result["word_node_id"] > 0:
				if debug > 0:
					print("found word in wn: ", search_word, word, word_result["word_node_id"])
				word_node = word_result["word_node"]
				if "suffix" in results:
					results["suffix"][0]["form"] = search_word
					results["suffix"][0]["db_form"] = word_node[0]["name"]
					results["suffix"][0]["wn_result"] = word_result
				else:
					result = {
						"form": search_word,
						"db_form": word_node[0]["name"],
						"wn_result": word_result
					}
					results["suffix"] = []
					results["suffix"].append(result)
				if "root" in results:
					#results["root"][0]["form"] = ""
					results["root"][0] = None
				results["prefix"][0]["form"] = prefix
				results["prefix"][0]["meaning"] = prefixes[pfx]["meaning"]
				if morphemes.format_results(results, "") == word:
					results["unmatched_char_count"] = 0
					break
	return results

def find_entry_in_db_given_suffix_and_prefix(word, prior_results):
	results = prior_results.copy()
	if "suffix" in results and "prefix" in results:
		suffixes = results["suffix"][0]["all_entries"]
		prefixes = results["prefix"][0]["all_entries"]

		oktocontinue = True
		for sfx in suffixes:
			if oktocontinue:
				for pfx in prefixes:
					if oktocontinue:
						suffix = suffixes[sfx]["form"]
						prefix = prefixes[pfx]["form"]
						prefix_plus_root_len = len(word) - len(suffix)
						prefix_plus_root = word[:prefix_plus_root_len]
						search_word = prefix_plus_root[len(prefix):]
						word_result = find_word_in_db(search_word)
						if word_result != None and word_result["word_node_id"] > 0:
							if debug > 0:
								print("found word in wn: ", search_word, word, word_result["word_node_id"])
							word_node = word_result["word_node"]
							if "root" in results:
								results["root"][0]["form"] = search_word
								results["root"][0]["db_form"] = word_node[0]["name"]
								results["root"][0]["wn_result"] = word_result
							else:
								result = {
									"form": search_word,
									"db_form": word_node[0]["name"],
									"wn_result": word_result
								}
								results["root"] = []
								results["root"].append(result)
							results["prefix"][0]["form"] = prefix
							results["prefix"][0]["meaning"] = prefixes[pfx]["meaning"]
							results["suffix"][0]["form"] = suffix
							results["suffix"][0]["meaning"] = suffixes[sfx]["meaning"]
							if morphemes.format_results(results, "") == word:
								results["unmatched_char_count"] = 0
								oktocontinue = False
	return results

def find_word_in_db(search_word):
	ret_result = {
		"form": search_word,
		"word_node_id": -1,
		"word_node": None
	}
	word_node_id, word_node = get_node_by_name(search_word) #NB multiple nodes
	if word_node_id > 0:
		ret_result["word_node_id"] = word_node_id
		ret_result["word_node"] = word_node
		return ret_result
	elif search_word[len(search_word)-1] in morphemes.consonants:
		for word_ending in ["e", "y"]:
			temp_search_word = search_word + word_ending
			word_node_id, word_node = get_node_by_name(temp_search_word)
			if word_node_id > 0:
				if debug > 0:
					print("found word in wn: ", temp_search_word, word_node_id)
				ret_result["word_node_id"] = word_node_id
				ret_result["word_node"] = word_node
				ret_result["temp_form"] = temp_search_word
				break
		return ret_result

def lkup_wn(word):
	synsets = wn.synsets(word)
	ret_synsets = []
	#print(synsets)
	for synset in synsets:
		ret_hyponyms = []
		for hn in synset.hyponyms():
			hn_o = {
				"name": hn.name(),
				"lemma": hn.name().split('.')[0],
				"pos": hn.pos()
			}
			ret_hyponyms.append(hn_o)
		ret_synset = {
			"name": synset.name(),
			"definition": synset.definition(),
			"pos": synset.pos(),
			"lemma_names": synset.lemma_names(),
			"hypernyms": synset.hypernyms(),
			"root_hypernyms": synset.root_hypernyms(),
			"hypernym_paths": synset.hypernym_paths(),
			"hyponyms": ret_hyponyms,  #synset.hyponyms(),
			"part_meronyms": synset.part_meronyms(),
			"substance_meronyms": synset.substance_meronyms(),
			"part_holonyms": synset.part_holonyms(),
			"part_holonyms": synset.part_holonyms(),
			"entailments": synset.entailments(),
			"min_depth": synset.min_depth()
		}
		ret_synsets.append(ret_synset)
	return ret_synsets

def get_node_by_name(word):
	synsets = lkup_wn(word)
	l = len(synsets)
	return l, synsets
