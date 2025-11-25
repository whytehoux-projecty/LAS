import { useState, useEffect, useRef } from 'react';

export type StreamMessage = {
    type: string;
    data: any;
};

export function useAgentStream() {
    const [messages, setMessages] = useState<StreamMessage[]>([]);
    const [isConnected, setIsConnected] = useState(false);
    const eventSourceRef = useRef<EventSource | null>(null);

    useEffect(() => {
        // Initialize EventSource
        const url = process.env.NEXT_PUBLIC_API_URL
            ? `${process.env.NEXT_PUBLIC_API_URL}/stream`
            : 'http://localhost:8000/stream';

        const eventSource = new EventSource(url);
        eventSourceRef.current = eventSource;

        eventSource.onopen = () => {
            setIsConnected(true);
            console.log('Connected to LAS stream');
        };

        eventSource.onmessage = (event) => {
            try {
                const parsedData = JSON.parse(event.data);
                setMessages((prev: StreamMessage[]) => [...prev, parsedData]);
            } catch (error) {
                console.error('Error parsing stream message:', error);
            }
        };

        eventSource.onerror = (error) => {
            console.error('Stream error:', error);
            eventSource.close();
            setIsConnected(false);
            // Optional: Implement reconnection logic here
        };

        return () => {
            eventSource.close();
            setIsConnected(false);
        };
    }, []);

    return { messages, isConnected };
}
