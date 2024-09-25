def find_missing_and_repeated_entries(runs, runDigits, subruns, subrunDigits, separator, l_entries = []):
    # Create a set of all expected entries
    expected_entries = set()
    for run in range(runs):
        run_padded = str(run).zfill(runDigits)
        for subrun in range(subruns):
            subrun_padded = str(subrun).zfill(subrunDigits)
            expected_entries.add(run_padded + separator + subrun_padded)

    # Create a set of actual entries
    actual_entries = set(entries)

    # Find the missing entries
    missing_entries = expected_entries - actual_entries

    # Find the repeated entries
    repeated_entries = {entry for entry in actual_entries if entries.count(entry) > 1}

    return missing_entries, repeated_entries

# Define the number of runs, number of digits for runs, number of subruns, number of digits for subruns, and the separator
runs = 2
runDigits = 4
subruns = 5
subrunDigits = 2
separator = "-"

# Example list of entries
entries = [
    '0000-00',
    '0000-01',
    '0000-03',
    '0001-00',
    '0001-02',
    '0001-03',
    '0001-04',
    '0001-04'
]

# Find missing entries and repeated entries
missing, repeated = find_missing_and_repeated_entries(runs, runDigits, subruns, subrunDigits, separator, entries)

print("Missing Entries:")
for entry in missing:
    print(entry)

print("\nRepeated Entries:")
for entry in repeated:
    print(entry)

