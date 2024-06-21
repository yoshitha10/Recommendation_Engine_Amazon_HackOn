import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const Recommendation: React.FC = () => {
  const [productId, setProductId] = useState('');
  const [messages, setMessages] = useState<{ sender: string, text: string }[]>([]);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const handleRecommend = async () => {
    if (!productId) {
      const errorMessage = { sender: 'bot', text: 'Enter a valid product ID' };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
      return;
    }

    const userMessage = { sender: 'user', text: `Product ID: ${productId}` };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    try {
      const res = await axios.post('http://127.0.0.1:5000/recommend', { product_id: productId });
      let newMessages;
      if (res.data.error) {
        const errorBotMessage = { sender: 'bot', text: res.data.error };
        newMessages = [...messages, userMessage, errorBotMessage];
      } else {
        const recommendationMessage = {
          sender: 'bot',
          text: `<strong>Payment Method:</strong> ${res.data.payment_method}<br /><strong>Cashback:</strong> ${res.data.cashback}<br /><strong>Success Rate:</strong> ${res.data.success_rate}`
        };
        newMessages = [...messages, userMessage, recommendationMessage];
      }
      setMessages(newMessages);
    } catch (err) {
      let errorMessage = 'An unexpected error occurred';
      if (axios.isAxiosError(err)) {
        if (err.response && err.response.data && err.response.data.error) {
          errorMessage = err.response.data.error;
        }
      }
      const errorBotMessage = { sender: 'bot', text: errorMessage };
      setMessages((prevMessages) => [...prevMessages, userMessage, errorBotMessage]);
    }

    setProductId('');
  };

  const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      handleRecommend();
    }
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <div className="recommendation p-4 bg-gray-100 rounded-lg shadow-md">
      <div className="messages-container p-4 bg-white rounded-md shadow-inner overflow-y-scroll h-96">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender === 'user' ? 'text-right' : 'text-left'} mb-2`}>
            <div 
              className={`inline-block p-2 rounded-md ${msg.sender === 'user' ? 'bg-green-600 text-white' : 'bg-gray-300 text-black'}`}
              dangerouslySetInnerHTML={{ __html: msg.text }}
            ></div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="mt-4 flex space-x-2">
        <input
          type="text"
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
          onKeyPress={handleKeyPress}
          className="flex-grow p-2 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500"
          placeholder="Enter Product ID"
        />
        <button 
          type="submit"
          onClick={handleRecommend} 
          className="p-2 bg-green-500 text-white rounded-md hover:bg-green-700"
        >
          Recommend Payment Method
        </button>
      </div>
    </div>
  );
};

export default Recommendation;
