import React from 'react';
import Recommendation from './components/Recommendation';

const App: React.FC = () => {
    return (
        <div className="app container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">AI Chatbot and Recommendation System</h1>
            <div className="w-full">
                <Recommendation />
            </div>
        </div>
    );
};

export default App;
