import tkinter as tk
from tkinter import ttk, font
import difflib

class AuroraAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AURORA // Neural AI Assistant")
        self.root.geometry("650x780")
        self.root.config(bg="#0b1329")

        # Top Header Bar (Aurora Style)
        header_frame = tk.Frame(root, bg="#111c3a", pady=14, padx=20)
        header_frame.pack(fill=tk.X)
        
        # Simulated AI Avatar Icon
        avatar_lbl = tk.Label(header_frame, text="AI", font=("Segoe UI", 10, "bold"), bg="#3b82f6", fg="#ffffff", padx=8, pady=4)
        avatar_lbl.pack(side=tk.LEFT)
        
        title_container = tk.Frame(header_frame, bg="#111c3a")
        title_container.pack(side=tk.LEFT, padx=12)
        
        tk.Label(title_container, text="AURORA", font=("Segoe UI", 11, "bold"), bg="#111c3a", fg="#ffffff").pack(anchor=tk.W)
        
        status_row = tk.Frame(title_container, bg="#111c3a")
        status_row.pack(anchor=tk.W)
        tk.Label(status_row, text="●", font=("Segoe UI", 8), bg="#111c3a", fg="#22c55e").pack(side=tk.LEFT)
        tk.Label(status_row, text=" Online", font=("Segoe UI", 8), bg="#111c3a", fg="#94a3b8").pack(side=tk.LEFT)

        # Main Scrollable Chat Container (Bubble UI)
        self.chat_container = tk.Canvas(root, bg="#0b1329", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.chat_container.yview)
        
        self.scrollable_frame = tk.Frame(self.chat_container, bg="#0b1329")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chat_container.configure(scrollregion=self.chat_container.bbox("all"))
        )

        self.chat_container.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.chat_container.configure(yscrollcommand=self.scrollbar.set)

        self.chat_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=15, pady=15)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bottom Input Control Bar (Pill Shape UI)
        input_wrapper = tk.Frame(root, bg="#0b1329", pady=15, padx=20)
        input_wrapper.pack(fill=tk.X, side=tk.BOTTOM)

        input_pill = tk.Frame(input_wrapper, bg="#1a264e", highlightbackground="#3b82f6", highlightthickness=1)
        input_pill.pack(fill=tk.X, ipady=6, ipadx=10)

        # Attachment / Mic icon placeholders (Visual styling)
        tk.Label(input_pill, text="📎", font=("Segoe UI", 11), bg="#1a264e", fg="#94a3b8").pack(side=tk.LEFT, padx=(5, 8))
        
        self.user_entry = tk.Entry(input_pill, font=("Segoe UI", 11), bg="#1a264e", fg="#ffffff", 
                                   insertbackground="#ffffff", relief=tk.FLAT, bd=0)
        self.user_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.user_entry.bind("<Return>", lambda event: self.handle_user_message())
        
        send_btn = tk.Button(input_pill, text="➔", font=("Segoe UI", 12, "bold"), 
                             bg="#3b82f6", fg="#ffffff", activebackground="#2563eb", activeforeground="#ffffff",
                             relief=tk.FLAT, padx=12, pady=2, command=self.handle_user_message)
        send_btn.pack(side=tk.RIGHT, padx=2)

        # Initial Greeting from Aurora
        self.add_message("AURORA", "Greetings! I'm always evolving. My latest update includes enhanced natural language understanding and personalized recommendations.")

    def add_message(self, sender, text):
        # Frame for individual message bubble row
        msg_row = tk.Frame(self.scrollable_frame, bg="#0b1329", pady=6)
        msg_row.pack(fill=tk.X, expand=True)

        if sender == "USER":
            # User Bubble (Aligned Right, Dark/Light Blue contrast)
            bubble = tk.Frame(msg_row, bg="#2563eb", padx=14, pady=10)
            bubble.pack(side=tk.RIGHT, anchor=tk.E, padx=(50, 0))
            
            lbl = tk.Label(bubble, text=text, font=("Segoe UI", 10), bg="#2563eb", fg="#ffffff", wraplength=400, justify=tk.LEFT)
            lbl.pack()
        else:
            # AI/Aurora Bubble (Aligned Left, Deep Slate/Purple contrast like reference image)
            bubble = tk.Frame(msg_row, bg="#1e293b", padx=14, pady=10)
            bubble.pack(side=tk.LEFT, anchor=tk.W, padx=(0, 50))
            
            lbl = tk.Label(bubble, text=text, font=("Segoe UI", 10), bg="#1e293b", fg="#e2e8f0", wraplength=400, justify=tk.LEFT)
            lbl.pack()

        # Auto scroll to bottom
        self.chat_container.update_idletasks()
        self.chat_container.yview_moveto(1.0)

    def generate_response(self, query):
        q = query.lower().strip()
        
        # Small Talk & Greetings
        if any(w in q for w in ["hi", "hello", "hey", "greetings", "hii"]):
            return "Hello there! How can I assist you with your project or queries today?"
        if any(w in q for w in ["how are you", "aur batao"]):
            return "I'm operating at peak efficiency! Ready to help you build or test amazing things."
        if any(w in q for w in ["bye", "exit", "quit", "goodbye"]):
            return "Goodbye! Feel free to reach out whenever you need assistance again."
        if any(w in q for w in ["thank", "thanks", "thx"]):
            return "You're very welcome! Let me know if you need anything else."
        
        # Features / Latest updates query (matching reference image concept)
        if any(w in q for w in ["feature", "latest", "update", "what's new", "capabilities"]):
            return "Certainly! I can now integrate with more apps, offer proactive assistance, and generate creative content or handle technical queries."

        # Knowledge Base / FAQs
        faqs = {
            "return policy": "You can return any product within 30 days of purchase for a full refund, provided it is in original packaging.",
            "track order": "Once dispatched, you will receive an SMS and email containing your live tracking link.",
            "payment methods": "We accept credit/debit cards, UPI (Google Pay, PhonePe), PayPal, and Cash on Delivery (COD).",
            "reset password": "Click on 'Forgot Password' on the login screen, enter your registered email, and follow the secure reset link.",
            "customer support": "Yes! Our dedicated support crew is online 24/7 via live chat, email, and phone helpline."
        }

        for key, ans in faqs.items():
            if key in q:
                return ans

        # Fuzzy Matching for typos
        matches = difflib.get_close_matches(q, list(faqs.keys()), n=1, cutoff=0.3)
        if matches:
            return f"Did you mean {matches[0]}? Here is the info: {faqs[matches[0]]}"

        return "I'm still learning! Could you please rephrase your question or ask about our core services, returns, or tracking?"

    def handle_user_message(self):
        text = self.user_entry.get()
        if not text.strip():
            return
        
        # Add User Message to UI
        self.add_message("USER", text)
        self.user_entry.delete(0, tk.END)
        
        # Generate & Add AI Response
        response = self.generate_response(text)
        self.root.after(300, lambda: self.add_message("AURORA", response))

if __name__ == "__main__":
    root = tk.Tk()
    app = AuroraAIApp(root)
    root.mainloop()