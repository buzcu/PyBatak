"""Module for managing card images in a GUI application."""
import tkinter as tk
from dataclasses import dataclass, field
from batak import Card
from PIL import Image, ImageTk

@dataclass(order=True, frozen=False)
class CardFaces:
    """Class to manage loading and retrieving card images."""
    image_directory = "cards/"
    images: dict[Card, ImageTk.PhotoImage] = field(default_factory=dict)
    back_image_vertical: ImageTk.PhotoImage = field(init=False, default=None)
    back_image_horizontal: ImageTk.PhotoImage = field(init=False, default=None)

    def load_images(self, image_directory: str = None):
        """Load card images from the specified directory."""
        if image_directory is None:
            image_directory = self.image_directory

        for suit in Card.VALID_SUITS:
            for rank in range(2, 15):
                card = Card(suit=suit, rank=rank)
                filename = f"{image_directory}{suit} {rank}.png"
                try:
                    pil_image = Image.open(filename)
                    pil_image = pil_image.convert("RGBA")
                    pil_image = pil_image.resize((75, 105), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(pil_image)
                    self.images[card] = image
                except Exception as e:
                    print(f"Error loading image for {card}: {e}")
        try:
            back_image_v = Image.open(f"{image_directory}cardbackdesignvertical_small.png")
            back_image_h = Image.open(f"{image_directory}cardbackdesignhorizontal_small.png")
            back_image_v = back_image_v.convert("RGBA")
            back_image_h = back_image_h.convert("RGBA")
            back_photo_v = ImageTk.PhotoImage(back_image_v)
            back_photo_h = ImageTk.PhotoImage(back_image_h)
            self.back_image_vertical = back_photo_v
            self.back_image_horizontal = back_photo_h
        except Exception as e:
            print(f"Error loading back card images: {e}")

    def get_image(self, card_obj: object) -> tk.PhotoImage:
        """Retrieves the image using the Card object itself."""
        return self.images.get(card_obj)
    
    def get_back_image_vertical(self) -> tk.PhotoImage:
        """Retrieves the back image of the card."""
        return self.back_image_vertical
    
    def get_back_image_horizontal(self) -> tk.PhotoImage:
        """Retrieves the back image of the card."""
        return self.back_image_horizontal