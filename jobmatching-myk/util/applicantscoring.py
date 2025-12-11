from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import Normalizer


class ApplicantScorer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.normalizer = Normalizer()

    def fit(self, job_descriptions):
        # Fit the vectorizer on the job descriptions
        self.vectorizer.fit(job_descriptions)

    def transform(self, resumes, job_descriptions):
        # Vectorize resumes and job descriptions
        resume_vectors = self.vectorizer.transform(resumes)
        job_vectors = self.vectorizer.transform(job_descriptions)

        # Normalize the vectors
        normalized_resume_vectors = self.normalizer.transform(resume_vectors)
        normalized_job_vectors = self.normalizer.transform(job_vectors)

        # Calculate similarity scores
        similarity_scores = cosine_similarity(normalized_resume_vectors, normalized_job_vectors)
        return similarity_scores

    def score_applicants(self, resumes, job_descriptions):
        # Ensure that vectorizer is fitted before transforming
        if not hasattr(self.vectorizer, 'vocabulary_'):
            raise ValueError(
                "The vectorizer is not fitted. Call 'fit' with job descriptions before scoring applicants.")

        # Get similarity scores
        similarity_scores = self.transform(resumes, job_descriptions)

        # Derive scores, assuming now multiple job descriptions are possible
        scores = [max(score) for score in similarity_scores]  # Get the maximum similarity score for each resume
        return scores


# Example Usage
def initialize_scorer(job_description):
    scorer = ApplicantScorer()
    scorer.fit([job_description])
    return scorer
