import React, { useState } from 'react';
import { Brain, Calendar, Clock, MapPin, BookOpen, Bell, MessageSquare, Bot, ChevronRight, ChevronLeft, HelpCircle, Sparkles } from 'lucide-react';

function FeatureCard({ icon: Icon, title, description }: { icon: React.ElementType, title: string, description: string }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 hover:bg-gradient-to-br hover:from-indigo-50 hover:to-white">
      <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center mb-4">
        <Icon className="w-6 h-6 text-white" />
      </div>
      <h3 className="text-xl font-semibold mb-2 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}

const conversations = [
  {
    question: "When's my next class?",
    answer: "Your next class is Introduction to Psychology at 2:00 PM in Room 301, Building B. Would you like directions to get there?"
  },
  {
    question: "What assignments are due this week?",
    answer: "You have 3 upcoming deadlines:\n1. Data Structures Essay (Tuesday)\n2. Physics Lab Report (Thursday)\n3. Web Development Project (Friday)\n\nWould you like me to set reminders for these?"
  },
  {
    question: "Can you help me find my lecture notes from last week?",
    answer: "I found these materials from last week:\n- Machine Learning Lecture 5 slides\n- Database Systems Chapter 7 notes\n- Programming Paradigms code examples\n\nWhich one would you like to access?"
  },
  {
    question: "What's my exam schedule for finals?",
    answer: "Here's your final exam schedule:\n- Monday: Calculus II (9:00 AM, Hall A)\n- Wednesday: Computer Networks (2:00 PM, Room 405)\n- Friday: Software Engineering (10:00 AM, Lab 3)\n\nShall I create a study schedule for you?"
  },
  {
    question: "How do I get to the Computer Science building?",
    answer: "The Computer Science building is located in the North Campus. From your current location, head east past the library, take the second right, and it will be the third building on your left. The walk should take about 8 minutes."
  }
];

function FaqItem({ question, answer }: { question: string, answer: string | JSX.Element }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="border-b border-indigo-100 last:border-none">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full py-4 flex items-center justify-between text-left hover:bg-indigo-50/50 rounded-lg px-4 transition-colors duration-200"
      >
        <span className="text-lg font-medium text-gray-800">{question}</span>
        <HelpCircle className={`w-5 h-5 text-indigo-500 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`} />
      </button>
      <div className={`overflow-hidden transition-all duration-300 ${isOpen ? 'max-h-96 pb-4' : 'max-h-0'}`}>
        <div className="px-4 text-gray-600">
          {answer}
        </div>
      </div>
    </div>
  );
}

function App() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [slideDirection, setSlideDirection] = useState<'left' | 'right'>('right');

  const nextSlide = () => {
    setSlideDirection('right');
    setCurrentSlide((prev) => (prev + 1) % conversations.length);
  };

  const prevSlide = () => {
    setSlideDirection('left');
    setCurrentSlide((prev) => (prev - 1 + conversations.length) % conversations.length);
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <header className="gradient-bg text-white px-4 py-16 md:py-24">
        <div className="max-w-4xl mx-auto text-center">
          <div className="flex items-center justify-center mb-8">
            <div className="animate-float bg-white/10 p-4 rounded-2xl backdrop-blur-sm">
              <Bot className="w-12 h-12 text-white" />
            </div>
            <h1 className="text-4xl md:text-6xl font-bold ml-4">MoodleMate</h1>
          </div>
          <p className="text-xl md:text-2xl text-indigo-100 mb-8">
            Your AI-powered academic assistant that makes university life easier
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a
              href="https://t.me/MoodleMateBot"
              className="bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold flex items-center hover:bg-indigo-50 transition-all duration-300 hover:scale-105 shadow-lg"
            >
              Start Using MoodleMate <ChevronRight className="ml-2 w-5 h-5" />
            </a>
          </div>
        </div>
      </header>

      {/* Main Features */}
      <section className="container mx-auto px-4 py-16 bg-gradient-to-b from-indigo-50 to-white">
        <h2 className="text-3xl font-bold text-center mb-12 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Why Choose MoodleMate?</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <FeatureCard
            icon={Calendar}
            title="Dynamic Schedule Management"
            description="Stay on top of your class schedule with real-time updates and changes"
          />
          <FeatureCard
            icon={MapPin}
            title="Campus Navigation"
            description="Never get lost again with intelligent campus navigation assistance"
          />
          <FeatureCard
            icon={BookOpen}
            title="Course Materials Organization"
            description="Access and organize your lecture materials effortlessly"
          />
          <FeatureCard
            icon={Bell}
            title="Smart Reminders"
            description="Get personalized reminders for assignments, quizzes, and deadlines"
          />
          <FeatureCard
            icon={Brain}
            title="AI-Powered Assistance"
            description="Receive personalized study recommendations and support"
          />
          <FeatureCard
            icon={Clock}
            title="Time Management"
            description="Optimize your study schedule and never miss important deadlines"
          />
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-gradient-to-br from-indigo-100 via-purple-50 to-indigo-50 py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">How MoodleMate Works</h2>
          <div className="max-w-3xl mx-auto relative">
            <div className={`bg-white/80 backdrop-blur-sm rounded-xl p-8 shadow-lg transition-all duration-500 slide-${slideDirection} h-[300px] overflow-y-auto`}>
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center mr-4">
                  <MessageSquare className="w-6 h-6 text-white" />
                </div>
                <div>
                  <p className="text-gray-700 mb-2">Ask MoodleMate:</p>
                  <p className="text-lg font-medium bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                    "{conversations[currentSlide].question}"
                  </p>
                </div>
              </div>
              <div className="border-l-4 border-indigo-600 pl-4 ml-12">
                <p className="text-gray-600 whitespace-pre-line">
                  {conversations[currentSlide].answer}
                </p>
              </div>
            </div>
            
            {/* Navigation Buttons */}
            <button 
              onClick={prevSlide}
              className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-6 bg-white/80 backdrop-blur-sm p-2 rounded-full shadow-lg hover:bg-indigo-50 transition-all duration-300 hover:scale-110"
            >
              <ChevronLeft className="w-6 h-6 text-indigo-600" />
            </button>
            <button 
              onClick={nextSlide}
              className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-6 bg-white/80 backdrop-blur-sm p-2 rounded-full shadow-lg hover:bg-indigo-50 transition-all duration-300 hover:scale-110"
            >
              <ChevronRight className="w-6 h-6 text-indigo-600" />
            </button>

            {/* Dots */}
            <div className="flex justify-center mt-6 gap-2">
              {conversations.map((_, index) => (
                <button
                  key={index}
                  onClick={() => {
                    setSlideDirection(index > currentSlide ? 'right' : 'left');
                    setCurrentSlide(index);
                  }}
                  className={`w-2 h-2 rounded-full transition-all duration-300 ${
                    index === currentSlide 
                      ? 'bg-gradient-to-r from-indigo-600 to-purple-600 w-4' 
                      : 'bg-gray-300 hover:bg-indigo-400'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16 bg-gradient-to-b from-white to-indigo-50">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                Frequently Asked Questions
              </h2>
              <p className="text-gray-600">
                Learn how MoodleMate revolutionizes your academic experience with AI
              </p>
            </div>

            <div className="space-y-2 bg-white/80 backdrop-blur-sm rounded-xl p-6 shadow-lg">
              <FaqItem
                question="What problems does MoodleMate solve?"
                answer="MoodleMate addresses key challenges faced by university students: managing dynamic class schedules, navigating large campuses, organizing course materials, tracking deadlines, and accessing personalized academic assistance. It acts as your personal academic assistant, helping reduce stress and improve academic performance."
              />
              <FaqItem
                question="How does MoodleMate use AI to help students?"
                answer={
                  <div className="space-y-3">
                    <p>MoodleMate leverages advanced AI in several ways:</p>
                    <ul className="list-disc pl-5 space-y-2">
                      <li><span className="font-medium">Natural Language Processing:</span> Understands and responds to your questions naturally, like asking about your next class or assignment deadlines.</li>
                      <li><span className="font-medium">Smart Scheduling:</span> AI analyzes your timetable to send timely reminders and updates about classes and deadlines.</li>
                      <li><span className="font-medium">Personalized Learning:</span> Learns from your interactions to provide customized study recommendations and resource suggestions.</li>
                      <li><span className="font-medium">Contextual Awareness:</span> Understands the context of your queries to provide relevant information about classes, assignments, or campus navigation.</li>
                    </ul>
                  </div>
                }
              />
              <FaqItem
                question="How does it integrate with university systems?"
                answer="MoodleMate seamlessly connects with SOLSS and Moodle to access your academic information, including class schedules, assignments, and course materials. The AI constantly monitors these systems for updates, ensuring you always have the latest information about your classes and deadlines."
              />
              <FaqItem
                question="What makes MoodleMate different from regular reminder apps?"
                answer={
                  <div className="space-y-3">
                    <p>MoodleMate goes beyond simple reminders with:</p>
                    <ul className="list-disc pl-5 space-y-2">
                      <li><span className="font-medium">Intelligent Assistance:</span> Provides context-aware help and answers questions about your academic schedule.</li>
                      <li><span className="font-medium">Proactive Support:</span> Anticipates your needs and sends relevant information before you ask.</li>
                      <li><span className="font-medium">Real-time Updates:</span> Automatically adjusts to schedule changes and deadline extensions.</li>
                      <li><span className="font-medium">Academic Integration:</span> Direct connection to university systems for accurate, up-to-date information.</li>
                    </ul>
                  </div>
                }
              />
              <FaqItem
                question="How does MoodleMate help with time management?"
                answer="MoodleMate uses AI to analyze your academic schedule and workload, sending smart reminders for classes, assignments, and exams. It helps break down large projects into manageable tasks, suggests optimal study times based on your schedule, and ensures you never miss important deadlines. The system adapts to your study patterns and preferences over time."
              />
            </div>

            <div className="mt-8 text-center">
              <a
                href="https://t.me/MoodleMateBot"
                className="inline-flex items-center gap-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:opacity-90 transition-opacity duration-300 shadow-lg"
              >
                <Sparkles className="w-5 h-5" />
                Try MoodleMate Now
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gradient-to-br from-gray-900 to-indigo-900 text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-indigo-200">© 2025 MoodleMate - Slush'd Hackathon Project</p>
          <div className="mt-4 flex items-center justify-center space-x-4">
            <a 
              href="https://t.me/MoodleMateBot" 
              className="text-indigo-300 hover:text-indigo-100 transition-colors flex items-center gap-2"
            >
              <Bot className="w-5 h-5" />
              Telegram Bot
            </a>
            <a 
              href="https://linktr.ee/daniy310" 
              className="text-indigo-300 hover:text-indigo-100 transition-colors"
              target="_blank"
              rel="noopener noreferrer"
            >
              Contact
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;