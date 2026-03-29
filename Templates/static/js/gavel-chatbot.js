/**
 * ============================================================
 * GAVEL CHATBOT - Button Animation & Chat Interface
 * ============================================================
 */

class GavelChatbot {
  constructor() {
    this.gavelBtn = document.querySelector('.gavel-button');
    this.chatPanel = document.querySelector('.chatbot-panel');
    this.closeBtn = document.querySelector('.chatbot-close');
    this.inputField = document.querySelector('.chatbot-input');
    this.sendBtn = document.querySelector('.chatbot-send-btn');
    this.messagesContainer = document.querySelector('.chatbot-messages');
    
    this.scrollTimeout = null;
    this.scrollIdleTime = 3000; // 3 seconds
    this.hasAnimated = false;
    this.isDragging = false;

    console.log('🎤 GavelChatbot initializing...', {
      gavelBtn: !!this.gavelBtn,
      chatPanel: !!this.chatPanel,
      closeBtn: !!this.closeBtn,
      inputField: !!this.inputField,
      sendBtn: !!this.sendBtn,
      messagesContainer: !!this.messagesContainer
    });

    this.init();
  }

  init() {
    if (!this.gavelBtn) {
      console.warn('❌ Gavel button not found!');
      return;
    }

    console.log('✓ GavelChatbot initialized successfully');

    // Scroll idle detection for thump animation
    window.addEventListener('scroll', () => this.handleScrollIdle());

    // Gavel button click
    if (this.gavelBtn) {
      this.gavelBtn.addEventListener('click', () => {
        console.log('🎯 Gavel button clicked!');
        this.toggleChatPanel();
      });
    }

    // Close button
    if (this.closeBtn) {
      this.closeBtn.addEventListener('click', () => {
        console.log('❌ Close button clicked');
        this.closeChat();
      });
    }

    // Send button
    if (this.sendBtn) {
      this.sendBtn.addEventListener('click', () => {
        console.log('📤 Send button clicked');
        this.sendMessage();
      });
    }

    // Input field Enter key
    if (this.inputField) {
      this.inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          console.log('📤 Enter key pressed');
          this.sendMessage();
        }
      });
    }
  }

  handleScrollIdle() {
    // Clear existing timeout
    clearTimeout(this.scrollTimeout);

    // Show scroll indicator
    if (this.gavelBtn) {
      this.gavelBtn.style.opacity = '0.5';
    }

    // Set new timeout
    this.scrollTimeout = setTimeout(() => {
      if (!this.hasAnimated && this.gavelBtn && !this.chatPanel?.classList.contains('is-open')) {
        this.triggerThump();
        this.hasAnimated = true;
      }
    }, this.scrollIdleTime);

    // Reset animation for next cycle
    window.addEventListener('scroll', () => {
      this.hasAnimated = false;
    }, { once: true });
  }

  triggerThump() {
    if (!this.gavelBtn) return;

    // Add thump animation
    this.gavelBtn.classList.add('is-thumping');
    
    // Create shockwave
    this.createShockwave();

    // Remove animation class
    setTimeout(() => {
      this.gavelBtn.classList.remove('is-thumping');
      if (this.gavelBtn) {
        this.gavelBtn.style.opacity = '1';
      }
    }, 600);
  }

  createShockwave() {
    const shockwave = document.createElement('div');
    shockwave.className = 'shockwave';
    document.body.appendChild(shockwave);

    setTimeout(() => {
      shockwave.remove();
    }, 800);
  }

  toggleChatPanel() {
    if (this.chatPanel) {
      const isOpen = this.chatPanel.classList.contains('is-open');
      console.log('💬 Toggling chat panel:', isOpen ? 'closing' : 'opening');
      this.chatPanel.classList.toggle('is-open');
      
      if (this.chatPanel.classList.contains('is-open') && this.inputField) {
        // Focus input after animation
        setTimeout(() => {
          this.inputField.focus();
          console.log('✓ Input focused');
        }, 200);
      }
    } else {
      console.warn('❌ Chat panel not found!');
    }
  }

  closeChat() {
    if (this.chatPanel) {
      this.chatPanel.classList.remove('is-open');
    }
  }

  async sendMessage() {
    if (!this.inputField || !this.inputField.value.trim()) {
      console.warn('⚠️ No message to send');
      return;
    }

    const userMessage = this.inputField.value.trim();
    this.inputField.value = '';

    console.log('📨 Sending message:', userMessage);

    // Add user message to chat
    this.addMessage(userMessage, 'user');

    // Disable input while processing
    this.inputField.disabled = true;
    this.sendBtn.disabled = true;

    try {
      // Send to backend API
      console.log('📡 Fetching /api/general-chat');
      const response = await fetch('/api/general-chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });

      console.log('📨 API response status:', response.status);

      if (response.ok) {
        const data = await response.json();
        console.log('✓ Got response:', data.response?.substring(0, 50) + '...');
        this.addMessage(data.reply || data.response || 'I received your message.', 'assistant');
      } else {
        console.error('❌ API returned error:', response.status);
        this.addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
      }
    } catch (error) {
      console.error('❌ Chat error:', error);
      this.addMessage('Connection error. Please try again later.', 'assistant');
    } finally {
      // Re-enable input
      this.inputField.disabled = false;
      this.sendBtn.disabled = false;
      this.inputField.focus();
    }
  }

  addMessage(text, sender = 'assistant') {
    if (!this.messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `message is-${sender}`;

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = text;

    messageDiv.appendChild(bubble);
    this.messagesContainer.appendChild(messageDiv);

    // Auto-scroll to bottom
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }

  destroy() {
    clearTimeout(this.scrollTimeout);
  }
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new GavelChatbot();
  });
} else {
  new GavelChatbot();
}
