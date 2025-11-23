import React from 'react';
import { ChatInterface } from '@/components/chat-interface';
import { TaskManager } from '@/components/task-manager';
import { MemoryViewer } from '@/components/memory-viewer';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col p-4 md:p-8 gap-6 bg-muted/10">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center text-primary-foreground font-bold">
            L
          </div>
          <h1 className="font-bold text-xl tracking-tight">LAS <span className="font-normal text-muted-foreground">Dashboard</span></h1>
        </div>
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <span>v2.0.0</span>
          <div className="h-4 w-[1px] bg-border"></div>
          <span className="flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-green-500"></span>
            System Online
          </span>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[calc(100vh-100px)]">

        {/* Left Column: Chat & Interaction (8 cols) */}
        <div className="lg:col-span-8 flex flex-col gap-6 h-full">
          <ChatInterface />
        </div>

        {/* Right Column: System State (4 cols) */}
        <div className="lg:col-span-4 flex flex-col gap-6 h-full overflow-hidden">
          <div className="h-1/2">
            <TaskManager />
          </div>
          <div className="h-1/2">
            <MemoryViewer />
          </div>
        </div>

      </div>
    </main>
  );
}
