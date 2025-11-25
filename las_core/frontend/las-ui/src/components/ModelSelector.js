import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ModelSelector.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:7777';

const PROVIDERS = [
    { id: 'ollama', name: 'Ollama (Local)' },
    { id: 'openrouter', name: 'OpenRouter' },
    { id: 'gemini', name: 'Google Gemini' },
    { id: 'groq', name: 'Groq' }
];

export const ModelSelector = ({ onModelChange, disabled }) => {
    const [provider, setProvider] = useState('ollama');
    const [model, setModel] = useState('tinydolphin');
    const [availableModels, setAvailableModels] = useState([]);
    const [isLoadingModels, setIsLoadingModels] = useState(false);
    const [customModel, setCustomModel] = useState('');

    useEffect(() => {
        fetchModels(provider);
    }, [provider]);

    useEffect(() => {
        // Notify parent of changes
        onModelChange({ provider, model: customModel || model });
    }, [provider, model, customModel, onModelChange]);

    const fetchModels = async (selectedProvider) => {
        setIsLoadingModels(true);
        try {
            const res = await axios.get(`${BACKEND_URL}/models?provider=${selectedProvider}`);
            setAvailableModels(res.data || []);

            // Set default model if current one isn't in list (unless using custom)
            if (res.data && res.data.length > 0) {
                if (!res.data.includes(model)) {
                    setModel(res.data[0]);
                }
            } else {
                // Fallbacks if list is empty
                if (selectedProvider === 'ollama') setModel('tinydolphin');
                if (selectedProvider === 'gemini') setModel('gemini-pro');
                if (selectedProvider === 'groq') setModel('llama3-8b-8192');
                if (selectedProvider === 'openrouter') setModel('anthropic/claude-3-opus');
            }
        } catch (err) {
            console.error("Error fetching models:", err);
            setAvailableModels([]);
        } finally {
            setIsLoadingModels(false);
        }
    };

    return (
        <div className="model-selector">
            <div className="selector-group">
                <label>Provider</label>
                <select
                    value={provider}
                    onChange={(e) => setProvider(e.target.value)}
                    disabled={disabled}
                >
                    {PROVIDERS.map(p => (
                        <option key={p.id} value={p.id}>{p.name}</option>
                    ))}
                </select>
            </div>

            <div className="selector-group">
                <label>Model</label>
                {availableModels.length > 0 ? (
                    <select
                        value={model}
                        onChange={(e) => {
                            setModel(e.target.value);
                            setCustomModel('');
                        }}
                        disabled={disabled || isLoadingModels}
                    >
                        {availableModels.map(m => (
                            <option key={m} value={m}>{m}</option>
                        ))}
                    </select>
                ) : (
                    <input
                        type="text"
                        placeholder="Enter model name"
                        value={customModel || model}
                        onChange={(e) => setCustomModel(e.target.value)}
                        disabled={disabled}
                    />
                )}
            </div>

            {provider === 'ollama' && (
                <div className="selector-group" style={{ flex: 0 }}>
                    <label>&nbsp;</label>
                    {/* Placeholder for Pull button logic if we implement backend endpoint for it */}
                </div>
            )}
        </div>
    );
};
