def shift_char(char, shift):
    if char.isalpha():
        # Determine if the character is uppercase or lowercase
        base = ord('A') if char.isupper() else ord('a')
        # Shift the character and wrap around using modulo
        return chr((ord(char) - base + shift) % 26 + base)
    return char

def encrypt(text, shift=3):
    # Define a substitution cipher using the specified symbols for lowercase and uppercase letters and digits
    substitution = {
        'a': 'ᑗ', 'b': 'ᑘ', 'c': 'ᑙ', 'd': 'ᑚ', 'e': 'ᑛ',
        'f': 'ᑜ', 'g': 'ᑝ', 'h': 'ᑞ', 'i': 'ᑟ', 'j': 'ᑠ',
        'k': 'ᑡ', 'l': 'ᑢ', 'm': 'ᑣ', 'n': 'ᑤ', 'o': 'ᑥ',
        'p': 'ᑦ', 'q': 'ᑧ', 'r': 'ᑨ', 's': 'ᑩ', 't': 'ᑪ',
        'u': 'ᑫ', 'v': 'ᑬ', 'w': 'ᑭ', 'x': 'ᑮ', 'y': 'ᑯ',
        'z': 'ᑰ',
        'A': 'ᑱ', 'B': 'ᑲ', 'C': 'ᑳ', 'D': 'ᑴ', 'E': 'ᑵ',
        'F': 'ᑶ', 'G': 'ᑷ', 'H': 'ᑸ', 'I': 'ᑹ', 'J': 'ᑺ',
        'K': 'ᑻ', 'L': 'ᑼ', 'M': 'ᑽ', 'N': 'ᑾ', 'O': 'ᑿ',
        'P': 'ᒀ', 'Q': 'ᒁ', 'R': 'ᒂ', 'S': 'ᒃ', 'T': 'ᒄ',
        'U': 'ᒅ', 'V': 'ᒆ', 'W': 'ᒇ', 'X': 'ᒈ', 'Y': 'ᒉ',
        'Z': 'ᒊ',
        '0': 'ᒋ', '1': 'ᒌ', '2': 'ᒍ', '3': 'ᒎ', '4': 'ᒏ',
        '5': 'ᒐ', '6': 'ᒑ', '7': 'ᒒ', '8': 'ᒓ', '9': 'ᒔ'
    }

    encrypted_text = ""

    for char in text:
        # Shift the character first if it's a letter
        shifted_char = shift_char(char, shift)
        # Apply substitution
        encrypted_text += substitution.get(shifted_char, shifted_char)

    return encrypted_text


def decrypt(text, shift=3):
    # Define the reverse substitution cipher
    reverse_substitution = {
        'ᑗ': 'a', 'ᑘ': 'b', 'ᑙ': 'c', 'ᑚ': 'd', 'ᑛ': 'e',
        'ᑜ': 'f', 'ᑝ': 'g', 'ᑞ': 'h', 'ᑟ': 'i', 'ᑠ': 'j',
        'ᑡ': 'k', 'ᑢ': 'l', 'ᑣ': 'm', 'ᑤ': 'n', 'ᑥ': 'o',
        'ᑦ': 'p', 'ᑧ': 'q', 'ᑨ': 'r', 'ᑩ': 's', 'ᑪ': 't',
        'ᑫ': 'u', 'ᑬ': 'v', 'ᑭ': 'w', 'ᑮ': 'x', 'ᑯ': 'y',
        'ᑰ': 'z',
        'ᑱ': 'A', 'ᑲ': 'B', 'ᑳ': 'C', 'ᑴ': 'D', 'ᑵ': 'E',
        'ᑶ': 'F', 'ᑷ': 'G', 'ᑸ': 'H', 'ᑹ': 'I', 'ᑺ': 'J',
        'ᑻ': 'K', 'ᑼ': 'L', 'ᑽ': 'M', 'ᑾ': 'N', 'ᑿ': 'O',
        'ᒀ': 'P', 'ᒁ': 'Q', 'ᒂ': 'R', 'ᒃ': 'S', 'ᒄ': 'T',
        'ᒅ': 'U', 'ᒆ': 'V', 'ᒇ': 'W', 'ᒈ': 'X', 'ᒉ': 'Y',
        'ᒊ': 'Z',
        'ᒋ': '0', 'ᒌ': '1', 'ᒍ': '2', 'ᒎ': '3', 'ᒏ': '4',
        'ᒐ': '5', 'ᒑ': '6', 'ᒒ': '7', 'ᒓ': '8', 'ᒔ': '9'
    }

    decrypted_text = ""

    for char in text:
        if char in reverse_substitution:  # Check if the character is a symbol
            # Apply reverse substitution
            original_char = reverse_substitution[char]
            # Reverse the shift
            decrypted_text += shift_char(original_char, -shift)
        else:
            # Non-symbol characters are added unchanged
            decrypted_text += char

    return decrypted_text