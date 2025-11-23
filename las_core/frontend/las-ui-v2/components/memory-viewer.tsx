"use client";

import React, { useState } from 'react';

type MemoryType = 'episodic' | 'semantic' | 'entity';

export function MemoryViewer() {
    const [activeTab, setActiveTab] = useState<MemoryType>('episodic');

    // Placeholder data - in real app, fetch from API
    const memories = {
        episodic: [
            { id: 1, content: "User asked to refactor the codebase.", timestamp: "2 mins ago" },
            { id: 2, content: "Analyzed AgenticSeek architecture.", timestamp: "1 hour ago" },
        ],
        semantic: [
            { id: 1, content: "LAS Architecture Overview", relevance: 0.95 },
            { id: 2, content: "React Component Patterns", relevance: 0.88 },
        ],
        entity: [
            { id: 1, name: "User", attributes: { role: "Admin", preference: "Dark Mode" } },
            { id: 2, name: "Project", attributes: { name: "LAS", status: "In Progress" } },
        ]
    };

    return (
        <div className="border rounded-xl bg-card text-card-foreground shadow-sm h-full flex flex-col">
            <div className="p-6 border-b">
                <h3 className="text-2xl font-semibold leading-none tracking-tight">Memory System</h3>
                <p className="text-sm text-muted-foreground mt-2">Inspect agent&apos;s internal state and knowledge.</p>
            </div>

            <div className="flex border-b">
                {(['episodic', 'semantic', 'entity'] as MemoryType[]).map((type) => (
                    <button
                        key={type}
                        onClick={() => setActiveTab(type)}
                        className={`flex-1 px-4 py-3 text-sm font-medium transition-colors hover:bg-muted/50 ${activeTab === type
                            ? 'border-b-2 border-primary text-primary'
                            : 'text-muted-foreground'
                            }`}
                    >
                        {type.charAt(0).toUpperCase() + type.slice(1)}
                    </button>
                ))}
            </div>

            <div className="p-6 flex-1 overflow-y-auto">
                <div className="space-y-4">
                    {activeTab === 'episodic' && memories.episodic.map((m: { id: number, content: string, timestamp: string }) => (
                        <div key={m.id} className="p-4 rounded-lg border bg-muted/20">
                            <p className="text-sm">{m.content}</p>
                            <p className="text-xs text-muted-foreground mt-2">{m.timestamp}</p>
                        </div>
                    ))}

                    {activeTab === 'semantic' && memories.semantic.map((m: { id: number, content: string, relevance: number }) => (
                        <div key={m.id} className="p-4 rounded-lg border bg-muted/20 flex justify-between items-center">
                            <span className="text-sm font-medium">{m.content}</span>
                            <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded-full">
                                {(m.relevance * 100).toFixed(0)}% Match
                            </span>
                        </div>
                    ))}

                    {activeTab === 'entity' && memories.entity.map((m: { id: number, name: string, attributes: Record<string, string | undefined> }) => (
                        <div key={m.id} className="p-4 rounded-lg border bg-muted/20">
                            <div className="flex items-center gap-2 mb-2">
                                <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">
                                    {m.name[0]}
                                </div>
                                <span className="font-medium">{m.name}</span>
                            </div>
                            <div className="grid grid-cols-2 gap-2 text-xs">
                                {Object.entries(m.attributes).map(([k, v]: [string, string | undefined]) => (
                                    <div key={k} className="bg-background p-2 rounded border">
                                        <span className="text-muted-foreground">{k}:</span> {v}
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
