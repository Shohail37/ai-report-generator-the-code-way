import os
from crew import build_crew
from pdf_export import convert_md_to_pdf

topic = input("Enter a research topic: ").strip()
print("\nRunning multi-agent pipeline... this can take 1-3 minutes.\n")

crew = build_crew(topic)
result = crew.kickoff()
report_text = str(result)

os.makedirs("outputs", exist_ok=True)
safe_name = topic.replace(" ", "_")[:40]

md_path = f"outputs/{safe_name}.md"
pdf_path = f"outputs/{safe_name}.pdf"

with open(md_path, "w", encoding="utf-8") as f:
    f.write(report_text)

convert_md_to_pdf(report_text, pdf_path)

print(f"\n✅ Report saved to {md_path}")
print(f"✅ PDF saved to {pdf_path}\n")