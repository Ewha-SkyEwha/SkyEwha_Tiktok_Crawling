import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

def cluster_hashtags(results, k=7):
    hashtags = [tag.lstrip("#") for tag, _ in results]
    posts = [cnt for _, cnt in results]

    n_samples = len(hashtags)
    if n_samples == 0:
        print("❌ 해시태그가 하나도 없습니다. 크롤링 실패!")
        return
    if n_samples == 1:
        print("❗ 해시태그가 1개만 수집되었습니다. 클러스터링 불가.")
        print(f"# {hashtags[0]} ({posts[0]})")
        return
    if n_samples < k:
        k = n_samples
        print(f"⚠️ 데이터가 {n_samples}개라서 클러스터 수 k를 {k}로 조정합니다.")

    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    embeddings = model.encode(hashtags)

    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    df = pd.DataFrame({
        "hashtag": hashtags,
        "posts": posts,
        "cluster": labels,
    })

    print(f"{'순위':<4} {'해시태그':<20} 게시글수   클러스터")
    for idx, row in df.iterrows():
        print(f"{idx+1:<4} #{row['hashtag']:<19} {row['posts']:<10} {row['cluster']}")

    for i in range(k):
        print(f"\n[클러스터 {i}]")
        print(df[df.cluster == i][["hashtag", "posts"]])

    # CSV 및 엑셀로 저장
    df.to_csv("travel_hashtags_clustered.csv", index=False, encoding="utf-8-sig")
    print("✅ travel_hashtags_clustered.csv 저장 완료!")

    return df