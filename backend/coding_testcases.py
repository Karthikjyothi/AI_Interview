HIDDEN_TESTS = {

    "move_zeroes": [
        {"input": "8\n4\n5\n0\n1\n9\n0\n5\n0", "expected": "4 5 1 9 5 0 0 0"},
        {"input": "6\n6\n0\n1\n8\n0\n2", "expected": "6 1 8 2 0 0"}
    ],

    "second_largest": [
        {"input": "6\n12\n45\n67\n45\n89\n67", "expected": "67"},
        {"input": "5\n10\n20\n30\n40\n50", "expected": "40"}
    ],

    "first_repeating": [
        {"input": "7\n4\n5\n1\n2\n5\n7\n1", "expected": "5"},
        {"input": "6\n9\n8\n7\n6\n8\n5", "expected": "8"}
    ],

    "missing_number": [
        {"input": "5\n1\n2\n3\n5", "expected": "4"},
        {"input": "6\n1\n2\n4\n5\n6", "expected": "3"}
    ],

    "palindrome": [
        {"input": "madam", "expected": "Palindrome"},
        {"input": "clock", "expected": "Not Palindrome"}
    ],

    "sum_excluding_minmax": [
        {"input": "5\n4\n8\n1\n9\n3", "expected": "15"},
        {"input": "6\n10\n2\n7\n5\n1\n9", "expected": "24"}
    ],

    "frequency_count": [
        {"input": "6\n2\n3\n2\n5\n3\n2", "expected": "2 -> 3\n3 -> 2\n5 -> 1"},
        {"input": "5\n1\n1\n1\n4\n4", "expected": "1 -> 3\n4 -> 2"}
    ],

    "kadane": [
        {"input": "8\n-2\n-3\n4\n-1\n-2\n1\n5\n-3", "expected": "7"},
        {"input": "5\n1\n2\n3\n4\n5", "expected": "15"}
    ],

    "first_non_repeating": [
        {"input": "22134514", "expected": "3"},
        {"input": "9988776", "expected": "6"}
    ],

    "manual_sort": [
        {"input": "5\n9\n2\n7\n1\n5", "expected": "1 2 5 7 9"},
        {"input": "4\n8\n3\n6\n4", "expected": "3 4 6 8"}
    ],

    "max_index": [
        {"input": "5\n10\n45\n22\n67\n31", "expected": "3"},
        {"input": "4\n99\n12\n54\n87", "expected": "0"}
    ],

    "below_average": [
        {"input": "5\n40\n60\n80\n20\n50", "expected": "2"},
        {"input": "4\n10\n20\n30\n40", "expected": "2"}
    ],

    "reverse_words": [
        {"input": "hello world from tcs", "expected": "olleh dlrow morf sct"},
        {"input": "smart coding round", "expected": "trams gnidoc dnuor"}
    ],

    "even_odd_rearrange": [
        {"input": "6\n5\n2\n8\n1\n9\n4", "expected": "2 8 4 5 1 9"},
        {"input": "5\n7\n6\n3\n2\n1", "expected": "6 2 7 3 1"}
    ],

    "repeat_missing": [
        {"input": "5\n1\n2\n2\n4\n5", "expected": "Repeated: 2 Missing: 3"},
        {"input": "6\n1\n3\n4\n5\n5\n6", "expected": "Repeated: 5 Missing: 2"}
    ],

    "longest_increasing": [
        {"input": "7\n10\n12\n14\n9\n11\n13\n15", "expected": "4"},
        {"input": "5\n5\n4\n3\n2\n1", "expected": "1"}
    ],

    "pair_sum_zero": [
        {"input": "5\n4\n-4\n7\n2\n1", "expected": "Yes"},
        {"input": "4\n1\n2\n3\n4", "expected": "No"}
    ],

    "caesar_cipher": [
        {"input": "abc\n2", "expected": "cde"},
        {"input": "xyz\n3", "expected": "abc"}
    ],

    "closest_pair_sum": [
        {"input": "5\n2\n7\n4\n9\n1\n10", "expected": "1 9"},
        {"input": "6\n5\n8\n12\n3\n7\n9\n15", "expected": "3 12"}
    ],

    "equilibrium_index": [
        {"input": "5\n1\n3\n5\n2\n2", "expected": "2"},
        {"input": "4\n1\n2\n3\n4", "expected": "-1"}
    ],

    "majority_element": [
        {"input": "7\n2\n2\n1\n2\n3\n2\n2", "expected": "2"},
        {"input": "5\n1\n2\n3\n4\n5", "expected": "-1"}
    ],

    "max_min_diff": [
        {"input": "5\n23\n45\n12\n67\n34", "expected": "55"},
        {"input": "4\n9\n9\n9\n9", "expected": "0"}
    ],

    "char_analysis": [
        {"input": "Tcs@123", "expected": "Vowels:0 Consonants:3 Digits:3 Special:1"},
        {"input": "Hello#9", "expected": "Vowels:2 Consonants:3 Digits:1 Special:1"}
    ],

    "array_palindrome": [
        {"input": "5\n1\n2\n3\n2\n1", "expected": "Palindrome"},
        {"input": "4\n1\n2\n3\n4", "expected": "Not Palindrome"}
    ],

    "binary_search": [
        {"input": "5\n10\n20\n30\n40\n50\n30", "expected": "Found"},
        {"input": "4\n5\n15\n25\n35\n20", "expected": "Not Found"}
    ],
    "pair_target_sum": [
        {
            "input": "5\n1\n4\n5\n6\n3\n7",
            "expected": "1 6\n4 3"
        },
        {
            "input": "4\n2\n8\n1\n9\n10",
            "expected": "2 8\n1 9"
        }
    ],
    "same_start_end_words": [
        {
            "input": "level madam test noon",
            "expected": "3"
        },
        {
            "input": "apple area code data",
            "expected": "2"
        }
    ],
        "second_smallest": [
        {"input": "5\n10\n4\n7\n2\n9", "expected": "4"},
        {"input": "6\n8\n1\n3\n5\n1\n9", "expected": "3"}
    ],

    "remove_duplicates": [
        {"input": "6\n2\n3\n2\n5\n3\n7", "expected": "2 3 5 7"},
        {"input": "5\n1\n1\n1\n2\n2", "expected": "1 2"}
    ],

    "longest_word": [
        {"input": "welcome to coding challenge", "expected": "challenge"},
        {"input": "tcs digital aptitude", "expected": "aptitude"}
    ],

    "array_rotation": [
        {"input": "5\n1\n2\n3\n4\n5\n2", "expected": "4 5 1 2 3"},
        {"input": "4\n10\n20\n30\n40\n1", "expected": "40 10 20 30"}
    ],

    "min_subarray": [
        {"input": "5\n3\n-4\n2\n-3\n-1", "expected": "-6"},
        {"input": "4\n1\n2\n3\n4", "expected": "1"}
    ],

    "descending_sort": [
        {"input": "5\n4\n9\n1\n7\n3", "expected": "9 7 4 3 1"},
        {"input": "4\n10\n2\n8\n6", "expected": "10 8 6 2"}
    ],

    "first_unique": [
        {"input": "7\n2\n2\n5\n3\n3\n8\n8", "expected": "5"},
        {"input": "5\n1\n1\n2\n2\n9", "expected": "9"}
    ],

    "position_digit_sum": [
        {"input": "1230", "expected": "Yes"},
        {"input": "9871", "expected": "No"}
    ],

    "peak_elements": [
        {"input": "6\n1\n5\n2\n8\n3\n1", "expected": "5 8"},
        {"input": "5\n9\n4\n7\n3\n2", "expected": "7"}
    ],

    "reverse_sentence": [
        {"input": "welcome to tcs", "expected": "tcs to welcome"},
        {"input": "coding is fun", "expected": "fun is coding"}
    ],

    "longest_consecutive_same": [
        {"input": "8\n1\n1\n1\n2\n2\n3\n3\n3", "expected": "3"},
        {"input": "6\n5\n5\n4\n4\n4\n1", "expected": "3"}
    ],

        "equal_partition": [
        {"input": "4\n1\n5\n5\n1", "expected": "Yes"},
        {"input": "4\n1\n2\n3\n5", "expected": "No"}
    ],

    "running_sum": [
        {"input": "5\n1\n2\n3\n4\n5", "expected": "1 3 6 10 15"},
        {"input": "4\n10\n-2\n3\n1", "expected": "10 8 11 12"}
    ],

    "digit_letter_separate": [
        {"input": "a1b2c3", "expected": "123 abc"},
        {"input": "x9y8", "expected": "98 xy"}
    ],

    "final_displacement": [
        {"input": "5\n10\n-3\n4\n-2\n1", "expected": "10"},
        {"input": "4\n5\n-10\n2\n1", "expected": "-2"}
    ],

    "count_primes": [
        {"input": "5\n2\n4\n5\n6\n7", "expected": "3"},
        {"input": "4\n8\n9\n10\n11", "expected": "1"}
    ],

    "neighbor_product": [
        {"input": "5\n2\n3\n4\n5\n6", "expected": "3 8 15 24 5"},
        {"input": "4\n1\n2\n3\n4", "expected": "2 3 8 3"}
    ],

    "duplicate_elements": [
        {"input": "6\n1\n2\n3\n2\n4\n1", "expected": "1 2"},
        {"input": "5\n5\n5\n6\n7\n7", "expected": "5 7"}
    ],

    "title_case": [
        {"input": "welcome to coding world", "expected": "Welcome To Coding World"},
        {"input": "tcs mock test", "expected": "Tcs Mock Test"}
    ],

    "median_value": [
        {"input": "5\n3\n1\n4\n2\n5", "expected": "3"},
        {"input": "4\n8\n6\n2\n10", "expected": "7.0"}
    ],

    "max_gap_start": [
        {"input": "5\n2\n10\n3\n20\n4", "expected": "3"},
        {"input": "4\n1\n5\n9\n2", "expected": "2"}
    ],

    "password_check": [
        {"input": "Tcs@1234", "expected": "Valid"},
        {"input": "tcs123", "expected": "Invalid"}
    ],

    "longest_decreasing": [
        {"input": "6\n9\n7\n5\n6\n4\n2", "expected": "3"},
        {"input": "5\n10\n8\n6\n4\n2", "expected": "5"}
    ],
        "zero_sum_subarray": [
        {"input": "6\n1\n2\n-3\n3\n-1\n2", "expected": "3"},
        {"input": "5\n4\n-4\n2\n-2\n1", "expected": "4"}
    ],

    "valid_palindrome_clean": [
        {"input": "A man, a plan, a canal, Panama", "expected": "Valid"},
        {"input": "OpenAI GPT", "expected": "Invalid"}
    ],

    "first_nonrepeat_char_string": [
        {"input": "aabbcddee", "expected": "c"},
        {"input": "xxyyzzk", "expected": "k"}
    ],

    "two_sum_indices": [
        {"input": "5\n2\n7\n11\n15\n3\n9", "expected": "0 1"},
        {"input": "4\n3\n2\n4\n6\n6", "expected": "1 2"}
    ],

    "longest_unique_substring": [
        {"input": "abcabcbb", "expected": "3"},
        {"input": "bbbb", "expected": "1"}
    ]
}