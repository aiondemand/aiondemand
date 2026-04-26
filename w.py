from aiod import get

paper_obj = get("https://arxiv.org/abs/1706.03762")

print(paper_obj)
print(paper_obj.fetch("estimators"))  # List of Estimator objects
print(paper_obj.fetch("datasets"))    # List of dataset names
print(paper_obj.fetch("metrics"))     # List of metric names
print(paper_obj.fetch("related_code_used"))
print(type(paper_obj))
