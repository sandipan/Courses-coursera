def randomStory(storyFile, wordTypes):
    ans = ""
    # write your code here
    import re, random

    words = open(storyFile).read()  # .split()
    words = re.split("(\W+?)", words)
    for word in words:
        if len(word) >= 1 and word[0] == "_":
            ans += "[ " + word[1:] + " ]"
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
