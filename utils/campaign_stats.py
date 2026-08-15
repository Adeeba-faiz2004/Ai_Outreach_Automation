def get_campaign_stats(results):

    total_leads = len(results)

    generated = sum(
        1
        for item in results
        if not item.get("failed", False)
    )

    sent = sum(
        1
        for item in results
        if item.get("sent", False)
    )

    failed = sum(
        1
        for item in results
        if item.get("failed", False)
    )

    skipped = sum(
        1
        for item in results
        if item.get("skipped", False)
    )

    return {
        "total": total_leads,
        "generated": generated,
        "sent": sent,
        "failed": failed,
        "skipped": skipped,
    }