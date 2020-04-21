import string
import collections

# vector of frequencies for english letters from our book
ENG_LETT_FREQ = [.082,.015,.028,.043,.127,.022,.020,.061,.070,.002,.008,.040,.024,.067,
                 .075,.019,.001,.060,.063,.091,.028,.010,.023,.001,.020,.001]
ALPHABET_ENCODING = [('a', 0), ('b', 1), ('c', 2), ('d', 3), ('e', 4), ('f', 5), ('g', 6), ('h', 7), ('i', 8), ('j', 9),
                     ('k', 10),('l', 11),('m', 12), ('n', 13),('o', 14), ('p', 15), ('q', 16), ('r',17), ('s', 18),
                     ('t', 19),('u', 20), ('v', 21),('w', 22), ('x', 23), ('y', 24), ('z', 25)]


# takes a text file to read and returns decrypted text
def analyze(ciphertext):
    with open(ciphertext, "r") as file:
        text = file.read()
    text = text.rstrip("\n")

    # get bigrams from the text
    n = 2
    bigrams = [text[i: i + n] for i in range(0, len(text), n)]
    biFreq = collections.Counter(bigrams)
    common = biFreq.most_common(len(text)/2)

    # save distances (could be any number) for 10 bigrams then take gcd of these distances,
    # giving the most probable key length
    # don't need to know bigram or anything like that, just take gcd
    # then split into columns by key length then perform bigram freq analysis
    distances = []
    for j in range(0, len(common) - 1):
        counter = 0
        pos_one = 0
        for i in range(0, len(bigrams)-1):
            if common[j][0] == bigrams[i]:
                counter = counter + 1
                if counter % 2 == 0:
                    distances.append(i - pos_one)
                pos_one = i

    # now that we have distances for all repeated bigrams, we can find the most common gcd.
    # this will give us the most probable key length
    common_gcds = []
    for i in range(0, len(distances) - 2):
        for j in range(i, len(distances)-2):
            gc = gcd(distances[i], distances[j+1])
            common_gcds.append(gc)

    # get some statistics on the most common gcds
    c_count = collections.Counter(common_gcds)
    out = c_count.most_common(5)

    # look for first most common gcd > 2, if it exists. This is our most probable key length
    most_common_gcd = 0
    for i in range(0, len(out) - 1):
        if out[i][0] > 2:
            most_common_gcd = out[i][0]
            break

    # now that we have our most common gcd, we can perform bigram frequency analysis based on these blocks
    print "Probable key length: ", most_common_gcd

    # get collections of characters in each shift position
    columns = [text[i::most_common_gcd] for i in range(most_common_gcd)]

    # now use the book's method with the maximal dot product between the frequency vector
    # and the shifted english letter frequency vector to get the key
    key = []
    decoded_key = []
    for index in range(0, len(columns)):
        w_vec = freq_analysis(columns[index], len(columns[i]))
        key.append(fitness(w_vec, ENG_LETT_FREQ))
        decoded_key.append(decode(fitness(w_vec, ENG_LETT_FREQ)))

    # print the key as a string so user can see what it is
    print "Probable key: ", (''.join(decoded_key))

    # output plaintext
    plaintext = decrypt(key, text)
    print "Decoded text: ", plaintext


# helper function for finding greatest common denominator
def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


# helper function to get a vector of frequencies for occurrences of english letters in a string
def freq_analysis(vector, length):
    freq_vec = []
    eng_alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']
    for idx in range(0, 26):
        freq_vec.append(float(vector.count(eng_alph[idx]))/float(length))
    return freq_vec


# helper function to shift english letter frequencies for determining fitness
def shift(vector, amount):
    vector_copy = list(vector)
    for index in range(0, amount):
        vector_copy.insert(0, vector_copy.pop())
    return vector_copy


# helper function for dot product
def dot_prod(x, y):
    if len(x) == len(y) and len(x) != 0:
        return sum([x[b] * y[b] for b in range(len(x))])
    else:
        return 0


# using the method from the book, find the highest value for the dot product and that is your shift for
# a given position
def fitness(vector, vector2):
    max_dot = 0
    saved_shift = 0
    for idx in range(0, len(vector)):
        dot = dot_prod(vector, shift(vector2, idx))
        if dot > max_dot:
            max_dot = dot
            saved_shift = idx
    return saved_shift


# to decode key (for demonstrative purposes)
def decode(number):
    for i in range(0, len(ALPHABET_ENCODING)):
        if ALPHABET_ENCODING[i][1] == number:
            return ALPHABET_ENCODING[i][0]


# to encode key (for demonstrative purposes)
def encode(letter):
    for i in range(0, len(ALPHABET_ENCODING)):
        if ALPHABET_ENCODING[i][0] == string.lower(letter):
            return ALPHABET_ENCODING[i][1]


# helper function to decrypt a given string of text once the key is found
def decrypt(key, text):
    j = 0
    text_copy = str()
    for i in range(0, len(text)):
        text_copy += str(decode((encode(text[i]) - key[j]) % 26))
        j = j + 1
        if j == len(key):
            j = 0
    return text_copy


def main():
    analyze("vig2.txt")


if __name__ == "__main__":
    main()
