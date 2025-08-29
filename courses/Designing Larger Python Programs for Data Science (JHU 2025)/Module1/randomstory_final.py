def randomStory(storyFile, wordTypes):
    ans = ""
    # write your code here
    import re, random

    cat_words = {}
    for word in wordTypes:
        cat_words[word] = open(f"{word}.txt").read().splitlines()
    # print(cat_words)
    words = open(storyFile).read()  # .split()
    words = re.split("(\W+?)", words)
    # print(words)
    fills = []
    for word in words:
        if len(word) >= 1 and word[0] == "_":
            fill = (
                random.choice(cat_words[word[1:]])
                if word[1:] in cat_words
                else fills[int(word[1:])]
            )
            fills.append(fill)
            ans += fill
        else:
            ans += word
    return ans


if __name__ == "__main__":
    categories = [
        "animal",
        "food",
        "greeting",
        "magiccreature",
        "place",
        "said",
        "thing",
        "time",
    ]
    print("Our first story is:")
    print("-" * 20)
    print(randomStory("story.txt", categories), end="")
    print("Our second story is:")
    print("-" * 20)
    print(randomStory("story2.txt", categories), end="")
    pass
