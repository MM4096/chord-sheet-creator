def convert_to_bool(input_str: str) -> bool:
	true_values = ["true", "t", "yes", "y", "1"]
	false_values = ["false", "f", "no", "n", "0"]
	combined_values = true_values + false_values

	if input_str.lower() in true_values:
		return True
	elif input_str.lower() in false_values:
		return False

	raise ValueError(f"Input must be one of {combined_values}")
