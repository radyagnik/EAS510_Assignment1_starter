"""EAS 510 - Project 1 - Phase 2: the V2 rule set (Rules 1-3 reweighted + Rule 4)."""

from functools import lru_cache

import numpy as np
import cv2

import rules

RULES = ("rule1_v2", "rule2_v2", "rule3_v2", "rule4_keypoints")

# Weights must sum to 100 (the format validator enforces Final Score == sum of scores).
W1, W2, W3, W4 = 15, 15, 30, 40


def _reweight(ev, new_out_of):
    """Keep the V1 rule's metric and fired flag; rescale its points to a new budget."""
    ev = dict(ev)
    ev["out_of"] = new_out_of
    ev["score"] = int(round(new_out_of * ev["metric"])) if ev["fired"] else 0
    return ev


def rule1_v2(target, input_path):
    return _reweight(rules.rule1_metadata(target, input_path), W1)


def rule2_v2(target, input_path):
    return _reweight(rules.rule2_histogram(target, input_path), W2)


def rule3_v2(target, input_path):
    return _reweight(rules.rule3_template(target, input_path), W3)


# ---- Rule 4: ORB keypoints + RANSAC (targets crops / resizing) ----
MAX_DIM = 640
MIN_INLIERS = 10     # fewer geometrically consistent matches than this = no evidence
FULL_INLIERS = 30    # this many or more = full points


@lru_cache(maxsize=64)
def _orb_features(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    h, w = img.shape[:2]
    s = MAX_DIM / float(max(h, w))
    if s < 1.0:
        img = cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    orb = cv2.ORB_create(nfeatures=1500)
    kp, des = orb.detectAndCompute(img, None)
    if des is None or len(kp) < 8:
        return None
    pts = np.float32([k.pt for k in kp])
    return pts, des


def rule4_keypoints(target, input_path):
    """Count keypoints in the suspect that match the original AND agree on one transform."""
    out = {"rule": 4, "name": "Keypoints", "fired": False, "score": 0,
           "out_of": W4, "note": "Keypoint score 0.00", "metric": 0.0}
    try:
        a = _orb_features(target["path"])
        b = _orb_features(input_path)
        if a is None or b is None:
            return out
        pts_o, des_o = a
        pts_s, des_s = b
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
        pairs = matcher.knnMatch(des_s, des_o, k=2)
        good = [m[0] for m in pairs
                if len(m) == 2 and m[0].distance < 0.75 * m[1].distance]
        inliers = 0
        if len(good) >= 4:
            src = pts_s[[g.queryIdx for g in good]].reshape(-1, 1, 2)
            dst = pts_o[[g.trainIdx for g in good]].reshape(-1, 1, 2)
            _, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
            if mask is not None:
                inliers = int(mask.sum())
        metric = min(1.0, inliers / float(FULL_INLIERS))
        out["metric"] = round(metric, 3)
        out["note"] = f"Keypoint score {out['metric']:.2f}"
        if inliers >= MIN_INLIERS:
            out["fired"] = True
            out["score"] = int(round(W4 * metric))
    except Exception:
        pass
    return out
