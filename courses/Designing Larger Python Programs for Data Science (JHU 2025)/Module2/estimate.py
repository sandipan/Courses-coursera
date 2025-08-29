import pandas as pd


def find_matches(df, card_list):
    # cards_col = df["Cards"].fillna("").astype(str)
    matches = pd.Series(True, index=df.index)
    for card in card_list:
        matches = matches & df["Cards"].str.contains(card)
        # Ensure card is exactly one of the tokens in the "Cards" column
        # matches &= cards_col.str.split().apply(lambda cards: card in cards)
    return matches


def estimate_one_file(fname, card_list):
    # use pandas to read the file called fname
    # use find_matches to get a Series of booleans
    # use that Series of booleans to filter the data
    # sum the filtered data with axis = 0 and numeric_only = True
    # compute the percentages  (totals / totals.sum() * 100)
    # return the percentages
    df = pd.read_csv(fname)
    # print(df.shape)
    matches = find_matches(df, card_list)
    df = df[matches]
    # print(df, df.shape)
    totals = df.sum(axis=0, numeric_only=True)
    # print(totals, totals.sum())
    percentages = totals / totals.sum() * 100
    return percentages


# df = pd.read_csv("subset.csv")
# df = df.dropna()
# matches = find_matches(df, ["As", "Ks", "Kh"])
# df = df[matches]
# print(df, df.shape)
# print(estimate_one_file("4card_mc.csv", ["As", "Ks", "Kh"]))
# totals = df.sum(axis=0, numeric_only=True)
# print(totals, totals.sum())
# percentages = totals / totals.sum() * 100
# print(percentages)


def estimate_many_files(fname_list, card_list):
    # For each file name in fname_list, use estimate_one_file
    # to estimate the probabilties for that file and card_list

    # put all the estimates into a list

    # use pd.concat to merge the estimates into one table
    # you will want axis=1 and keys=fname_list

    # return your merged table
    list_df = []
    for fname in fname_list:
        percentages = estimate_one_file(fname, card_list)
        list_df.append(percentages)
    merged_data = pd.concat(list_df, axis=1, keys=fname_list)
    return merged_data


if __name__ == "__main__":
    flist = ["4card_mc.csv", "3card_mc.csv", "true_probs.csv", "subset.csv"]
    card_lists = [["As", "Kh", "Ks"], ["8c", "7c", "6s"], ["Kc", "0c", "4c"]]
    for card_list in card_lists:
        ans = estimate_many_files(flist, card_list)
        print(f"For {card_list} we estimate")
        print(ans)
        pass
    pass
