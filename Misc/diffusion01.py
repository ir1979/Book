import torch
import torch.nn as nn
from torchvision.transforms import ToTensor, ToPILImage, Resize
from PIL import Image
from diffusers import DDPMPipeline, DDIMScheduler

# Load the pre-trained DDPM pipeline
model_id = "google/ddpm-celebahq-256"
pipeline = DDPMPipeline.from_pretrained(model_id)

# Move the model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device = 'cpu'
pipeline.to(device)

# Load and preprocess the degraded document image
degraded_image_path = "docs/degraded/51_1.processed.tif"
degraded_image = Image.open(degraded_image_path).convert("RGB")

# Resize the input image to a smaller resolution
degraded_image = Resize((256, 256))(degraded_image)
degraded_image_tensor = ToTensor()(degraded_image).unsqueeze(0).to(device)

# Use the DDIM scheduler with fewer timesteps
scheduler = DDIMScheduler(beta_start=0.0001, beta_end=0.02, beta_schedule="linear")
scheduler.set_timesteps(num_inference_steps=1000)

eta = 0.0  # Controls the amount of noise added during sampling (0.0 means no additional noise)

# Run the denoising process
with torch.no_grad():
    noisy_image = degraded_image_tensor
    for t in scheduler.timesteps:
        # Predict the noise residual
        model_output = pipeline.unet(noisy_image, t)["sample"]
        
        # Compute the previous noisy sample x_t -> x_{t-1}
        noisy_image = scheduler.step(model_output, t, noisy_image, eta=eta)["prev_sample"]
        print(t)

# Convert the denoised image tensor back to PIL Image
denoised_image_tensor = noisy_image.squeeze(0).cpu()
denoised_image = ToPILImage()(denoised_image_tensor)

# Save the denoised image
denoised_image_path = "./docs/output/51_1.processed_restored.tif"
denoised_image.save(denoised_image_path)
