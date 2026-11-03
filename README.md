
@staticmethod
def _should_snap_name(pred_l, cand):
    """
    Decide whether the predicted person name should be
    replaced by the authoritative eApp reference.

    Priority:
    1. Handle an extra repeated leading name token.
    2. Apply the existing fuzzy matching rules.

    Returns:
        (snap: bool, overlap: float, distance: int)
    """

    gt = cand.lower().strip()
    pred = pred_l.lower().strip()

    gt_words = set(gt.split())
    pred_words = set(pred.split())

    overlap = (
        len(gt_words & pred_words) / len(gt_words)
        if gt_words else 0.0
    )

    distance = Levenshtein.distance(gt, pred)

    # ==================================================
    # NEW: Repeated Leading Name Token
    # ==================================================
    gt_tokens = gt.split()
    pred_tokens = pred.split()

    if (
        len(gt_tokens) >= 2
        and len(pred_tokens) == len(gt_tokens) + 1
        and pred_tokens[1:] == gt_tokens
        and pred_tokens[0] == gt_tokens[-1]
    ):
        return True, overlap, distance

    # ==================================================
    # ORIGINAL: Fuzzy Matching (UNCHANGED)
    # ==================================================
    snap = (
        (overlap >= 0.5 and distance <= 3)
        or
        (overlap < 0.5 and distance <= 2)
    )

    return snap, overlap, distance
