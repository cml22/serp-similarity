def calculate_similarity(results1, results2):
    # Extract full URLs
    urls1 = {result[0]: result[1] for result in results1}
    urls2 = {result[0]: result[1] for result in results2}

    # Extract domains
    domains1 = {extract_domain(url): title for url, title in results1}
    domains2 = {extract_domain(url): title for url, title in results2}

    # Calculate similarity for URLs
    common_urls = set(urls1.keys()).intersection(set(urls2.keys()))
    non_common_urls1 = set(urls1.keys()) - common_urls
    non_common_urls2 = set(urls2.keys()) - common_urls
    total_urls = len(set(urls1.keys()).union(set(urls2.keys())))

    similarity_rate_url = (len(common_urls) / total_urls) * 100 if total_urls > 0 else 0

    # Calculate similarity for Domains (all URLs)
    common_domains = set(domains1.keys()).intersection(set(domains2.keys()))
    total_domains = len(set(domains1.keys()).union(set(domains2.keys())))
    similarity_rate_domain = (len(common_domains) / total_domains) * 100 if total_domains > 0 else 0

    # Calculate similarity for Domains with different URLs
    non_common_domains1 = {extract_domain(url) for url in non_common_urls1}
    non_common_domains2 = {extract_domain(url) for url in non_common_urls2}
    common_domains_diff_urls = non_common_domains1.intersection(non_common_domains2)
    total_non_common_domains = len(non_common_domains1.union(non_common_domains2))

    similarity_rate_domain_diff_urls = (len(common_domains_diff_urls) / total_non_common_domains) * 100 if total_non_common_domains > 0 else 0
    
    return (common_urls, non_common_urls1, non_common_urls2, similarity_rate_url,
            common_domains, non_common_domains1, non_common_domains2, similarity_rate_domain,
            common_domains_diff_urls, similarity_rate_domain_diff_urls)
