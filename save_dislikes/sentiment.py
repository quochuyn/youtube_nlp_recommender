# pred_sentiment.py

import numpy as np
import pandas as pd
import sklearn
import sklearn.ensemble

from time import perf_counter
import warnings
warnings.filterwarnings("ignore")

r"""
DISCLAIMER
----------
Much of the code is adapted from this repo: https://github.com/Jmete/youtube-dislikes
The folks behind the Save the Dislikes capstone trained a random forest model to 
predict whether an associated video was positive/negative. In essence, the model
tries to predict the dislike count or ratio of the associated video.
"""

# The model with no compression takes 1.5 seconds to load and is 945MB in size
# The model with 3 compression takes 3.6 seconds to load and is 188MB in size
# We are using the no compression for inference time but due to size limitations, we have the compressed version for github.



def _smooth_if_0(row):
    r"""
    Creates a smoothed `view_like` ratio feature to avoid division by zero for a more accurate 
    reflection of the ratio. 
    """

    if row["like_count"] == 0:
        vl_ratio = (row["view_count"]+1) / (row["like_count"]+1)
    else:
        vl_ratio = row["view_count"] / row["like_count"]
    return round(vl_ratio,2)



def make_pred(
        model : sklearn.ensemble.RandomForestClassifier, 
        pred_df : pd.DataFrame, 
        verbose : bool = True,
    ) -> np.ndarray:
    r"""
    Parameters
    ----------
    model : sklearn.ensemble.RandomForestClassifier
        The trained Random Forest Classifier model from the Save the Dislikes capstone.
    pred_df : pd.DataFrame
        The Youtube DataFrame of video data returned by youtube.get_youtube_data.search_youtube().
    verbose : bool, default=True
        Boolean value that controls the verbosity, the messages displayed.
    
    Returns
    -------
    preds : np.ndarray
        The predicted sentiment of the Youtube videos.
    """

    # Feature columns for classifier
    pred_df = pred_df.rename(columns={'video_duration':'duration', 'video_view_count':'view_count',
                            'video_like_count':'like_count', 'video_category_id':'cat_codes'})

    pred_df.loc[:,'view_like_ratio_smoothed'] = pred_df.apply(lambda row: _smooth_if_0(row), axis=1)

    X_cols = [
        "duration",
        "age_limit",
        "view_count",
        "like_count",
        "view_like_ratio_smoothed",
        "is_comments_enabled",
        "is_live_content",
        "cat_codes",
        "desc_neu",
        "desc_neg",
        "desc_pos",
        "desc_compound",
        "comment_neu",
        "comment_neg",
        "comment_pos",
        "comment_compound",
        "votes",
        "NoCommentsBinary"
    ]

    # if a column is missing, then fill with zeroes
    for col in X_cols:
        if col not in pred_df.columns:
            pred_df.loc[:,col] = 0

    if verbose:
        print("Making predictions...")
        start_pred_time = perf_counter()

    preds = model.predict(pred_df[X_cols])

    if verbose:
        print(f"  Time taken to make predictions: {(perf_counter() - start_pred_time):.4f} seconds")

    return preds



def sort_by_sentiment(
        model : sklearn.ensemble.RandomForestClassifier, 
        pred_df : pd.DataFrame, 
        verbose : bool = True,
    ) -> pd.DataFrame:
    r"""
    Parameters
    ----------
    model : sklearn.ensemble.RandomForestClassifier
        The trained Random Forest Classifier model from the Save the Dislikes capstone.
    pred_df : pd.DataFrame
        The Youtube DataFrame of video data returned by youtube.get_youtube_data.search_youtube().
    verbose : bool, default=True
        Boolean value that controls the verbosity, the messages displayed.
    
    Returns
    -------
    df : pd.DataFrame
        The sorted Youtube DataFrame by the Save the Dislikes sentiment scores.
    """

    preds = make_pred(model=model, pred_df=pred_df, verbose=verbose)
    pred_df.loc[:,'sentiment'] = preds

    # sort by sentiment
    non_negative_idx = pred_df[pred_df['sentiment'] != -1].index
    negative_idx = pred_df[pred_df['sentiment'] == -1].index
    sorted_idx = non_negative_idx.append(negative_idx)
    df = pred_df.iloc[sorted_idx]

    if verbose:
        num_negative_vids = len(negative_idx)

        if num_negative_vids == 0:
            print(f"\nNo negative videos found. No sorting occured.")
        else:
            print(f"\nMoved {num_negative_vids} videos to end of queue.")

    return df



def filter_out_sentiment(
        model : sklearn.ensemble.RandomForestClassifier, 
        pred_df : pd.DataFrame, 
        verbose : bool = True,
    ) -> pd.DataFrame:
    r"""
    Parameters
    ----------
    model : sklearn.ensemble.RandomForestClassifier
        The trained Random Forest Classifier model from the Save the Dislikes capstone.
    pred_df : pd.DataFrame
        The Youtube DataFrame of video data returned by youtube.get_youtube_data.search_youtube().
    verbose : bool, default=True
        Boolean value that controls the verbosity, the messages displayed.
    
    Returns
    -------
    df : pd.DataFrame
        The filtered Youtube DataFrame that removes any negative videos from the
        Save the Dislikes trained model.
    """

    preds = make_pred(model=model, pred_df=pred_df, verbose=verbose)
    pred_df.loc[:,'sentiment'] = preds

    # filter out negative (-1) videos
    df = pred_df[pred_df['sentiment'] != -1]

    return df


