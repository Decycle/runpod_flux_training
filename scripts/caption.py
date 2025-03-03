# def run_captioning(images, concept_sentence, *captions):
#     print(f"run_captioning")
#     print(f"concept sentence {concept_sentence}")
#     print(f"captions {captions}")
#     # Load internally to not consume resources for training
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     print(f"device={device}")
#     torch_dtype = torch.float16
#     model = AutoModelForCausalLM.from_pretrained(
#         "multimodalart/Florence-2-large-no-flash-attn", torch_dtype=torch_dtype, trust_remote_code=True
#     ).to(device)
#     processor = AutoProcessor.from_pretrained(
#         "multimodalart/Florence-2-large-no-flash-attn", trust_remote_code=True)

#     captions = list(captions)
#     for i, image_path in enumerate(images):
#         print(captions[i])
#         if isinstance(image_path, str):  # If image is a file path
#             image = Image.open(image_path).convert("RGB")

#         prompt = "<DETAILED_CAPTION>"
#         inputs = processor(text=prompt, images=image,
#                            return_tensors="pt").to(device, torch_dtype)
#         print(f"inputs {inputs}")

#         generated_ids = model.generate(
#             input_ids=inputs["input_ids"], pixel_values=inputs["pixel_values"], max_new_tokens=1024, num_beams=3
#         )
#         print(f"generated_ids {generated_ids}")

#         generated_text = processor.batch_decode(
#             generated_ids, skip_special_tokens=False)[0]
#         print(f"generated_text: {generated_text}")
#         parsed_answer = processor.post_process_generation(
#             generated_text, task=prompt, image_size=(image.width, image.height)
#         )
#         print(f"parsed_answer = {parsed_answer}")
#         caption_text = parsed_answer["<DETAILED_CAPTION>"].replace(
#             "The image shows ", "")
#         print(
#             f"caption_text = {caption_text}, concept_sentence={concept_sentence}")
#         if concept_sentence:
#             caption_text = f"{concept_sentence} {caption_text}"
#         captions[i] = caption_text

#         yield captions
#     model.to("cpu")
#     del model
#     del processor
#     if torch.cuda.is_available():
#         torch.cuda.empty_cache()
