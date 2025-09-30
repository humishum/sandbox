"""
Model: 4o 
Prompt: Using the manim library(https://www.manim.community/) , can you generate me code that can enable to learn deeply about the fast fourier transform? Assume I have knowledge of the fourier transform itself, but want to learn about the FFT itself. What is the math intuition behind it and how dows it work under the hood

honestly this isn't half bad! 
"""
from manim import *

class FFTIntuition(Scene):
    def construct(self):
        title = Title("Fast Fourier Transform (FFT) Intuition")
        self.play(Write(title))
        self.wait(1)

        # Step 1: DFT Equation
        dft_text = MathTex("X_k = \\sum_{n=0}^{N-1} x_n e^{-2\\pi i kn / N}")
        self.play(Write(dft_text))
        self.wait(1)

        # Step 2: Split into even and odd
        even_odd_text = MathTex(
            "X_k = \\sum x_{2n} e^{-2\\pi i k (2n)/N} + \\sum x_{2n+1} e^{-2\\pi i k (2n+1)/N}"
        ).next_to(dft_text, DOWN, buff=1)
        self.play(Transform(dft_text, even_odd_text))
        self.wait(2)

        # Step 3: Recursive Insight
        recursion = Tex("Recursive DFT on even and odd parts").next_to(even_odd_text, DOWN)
        arrow = Arrow(start=even_odd_text.get_bottom(), end=recursion.get_top())
        self.play(GrowArrow(arrow), Write(recursion))
        self.wait(1)

        # Step 4: Time complexity comparison
        time_text = Tex(r"Naive DFT: $\mathcal{O}(N^2)$ \quad vs \quad FFT: $\mathcal{O}(N \log N)$")
        time_text.to_edge(DOWN)
        self.play(Write(time_text))
        self.wait(2)

        # Step 5: Unit circle symmetry
        circle = Circle(radius=2)
        self.play(Create(circle))
        dots = VGroup()
        N = 8
        for k in range(N):
            angle = 2 * PI * k / N
            dot = Dot(point=[np.cos(angle)*2, np.sin(angle)*2, 0], color=YELLOW)
            dots.add(dot)
        self.play(AnimationGroup(*[FadeIn(dot) for dot in dots], lag_ratio=0.1))
        self.wait(1)

        # Fade out everything
        self.play(FadeOut(VGroup(title, dft_text, recursion, time_text, circle, dots)))

# Add CLI entry point
if __name__ == "__main__":
    from manim import config, tempconfig

    with tempconfig({
        "quality": "medium_quality",
        "disable_caching": True,
        "output_file": "fft_intuition.mp4"
    }):
        scene = FFTIntuition()
        scene.render()
