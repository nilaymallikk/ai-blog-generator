import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL_ID = "minimax/minimax-01"

def call_model(prompt, max_tokens=800, temperature=0.7):
    """
    Send prompt to MiniMax model through OpenRouter
    """
    try:
        response = client.responses.create(
            model=MODEL_ID,
            input=prompt,
            max_output_tokens=max_tokens,  
            temperature=temperature
        )
        return response.output_text
    except Exception as e:
        print("❌ Error calling model:", e)
        return ""

def generate_outline(topic, tone, audience):
    prompt = f"""
    You are a professional blog writer.
    Write a detailed outline for a blog on the topic: "{topic}".
    Tone: {tone}.
    Audience: {audience}.
    Include 4–6 main sections with sub-points.
    """
    return call_model(prompt, max_tokens=500, temperature=0.3)

def generate_section(topic, section_title, tone, audience):
    prompt = f"""
    Write a {tone} blog section for tech readers on the topic "{topic}".
    Section: "{section_title}".
    Make it informative and engaging.
    """
    return call_model(prompt, max_tokens=700, temperature=0.7)

def generate_blog(topic, tone="informal", audience="general"):
    print("\n🧠 Generating outline...")
    outline = generate_outline(topic, tone, audience)
    print("\n✅ Blog Outline:\n", outline)

    blog_content = f"# {topic}\n\n"

    if not outline.strip():
        print("⚠️ Outline generation failed.")
        return blog_content

    for i, line in enumerate(outline.splitlines()):
        if line.strip() and not line.strip().startswith("#"):
            print(f"\n✏️ Writing section {i+1}: {line.strip()}")
            section_text = generate_section(topic, line.strip(), tone, audience)
            blog_content += f"## {line.strip()}\n\n{section_text}\n\n"

    return blog_content

def main():
    print("=== 📝 Blog Generator (MiniMax M2 - Free) ===")
    topic = input("Enter blog topic (e.g. 'How to deploy a Flask app on Railway'): ").strip()
    tone = input("Tone (informal / professional / tutorial / narrative) [informal]: ").strip() or "informal"
    audience = input("Audience [general tech readers]: ").strip() or "general tech readers"

    final_blog = generate_blog(topic, tone, audience)

    # Save to file
    output_path = "generated_blog.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_blog)

    print(f"\n✅ Blog saved as: {output_path}")

if __name__ == "__main__":
    main()

