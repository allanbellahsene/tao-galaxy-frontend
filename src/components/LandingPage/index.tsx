import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Zap, ArrowRight, Compass, FileText, RssIcon, Bot, Users, ArrowUpRight, Github, Twitter, LineChart, Code, Search, BookOpen, BarChart, Rocket, Brain } from 'lucide-react';
import { fadeIn, staggerContainer } from './animations';

const LandingPage: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    setFormData({ name: '', email: '', message: '' });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  // Define common features for each role to ensure equal height
  const roleFeatures = {
    investors: [
      'Explore new opportunities visually',
      'Compare teams, traction, and transparency with AI-driven scores',
      'Stay ahead with real-time ecosystem updates',
      'Make smarter, faster allocation decisions'
    ],
    owners: [
      'Showcase your team, product, and progress',
      'Attract investors, miners, and collaborators',
      'Let your growth speak for itself through verified reports and news',
      'Build stronger community engagement' // Added to match length
    ],
    developers: [
      'Discover subnets with real traction',
      'Track launches and activity spikes',
      'Identify collaboration or reward opportunities with clarity',
      'Access comprehensive development resources' // Added to match length
    ]
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-sm border-b border-slate-800">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Zap className="text-indigo-500" size={24} />
              <span className="text-xl font-semibold bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-purple-500">TAO Galaxy</span>
            </div>
            <div className="flex items-center gap-6">
              <a href="#features" className="text-sm text-slate-300 hover:text-white transition-colors">Features</a>
              <a href="#about" className="text-sm text-slate-300 hover:text-white transition-colors">About</a>
              <Link to="/app" className="btn btn-primary bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500">
                Launch App
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <motion.section 
        variants={staggerContainer}
        initial="hidden"
        animate="show"
        className="min-h-screen flex items-center justify-center pt-16 relative overflow-hidden"
      >
        {/* Animated background elements */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(99,102,241,0.15),transparent_50%)]" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full border border-indigo-500/10 animate-[spin_60s_linear_infinite]" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full border border-purple-500/10 animate-[spin_40s_linear_infinite_reverse]" />
        </div>

        <div className="container mx-auto px-4 py-16 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div variants={fadeIn} className="mb-6">
              <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-indigo-500/10 to-purple-500/10 text-indigo-400 text-sm font-medium">
                <span>Powered by Bittensor</span>
                <ArrowRight size={16} />
              </span>
            </motion.div>
            
            <motion.h1 
              variants={fadeIn}
              className="text-5xl md:text-7xl font-bold mb-8 bg-clip-text text-transparent bg-gradient-to-r from-white via-indigo-200 to-purple-300 leading-tight"
            >
              The Intelligence Layer of Bittensor
            </motion.h1>
            
            <motion.p 
              variants={fadeIn}
              className="text-xl text-slate-300 mb-12 max-w-2xl mx-auto leading-relaxed"
            >
              Discover, evaluate, and stay updated on everything happening across the subnet galaxy.
            </motion.p>
            
            <motion.div variants={fadeIn} className="flex items-center justify-center gap-4">
              <Link 
                to="/app" 
                className="btn px-8 py-4 text-lg bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 rounded-xl shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:scale-105"
              >
                Explore the Galaxy
              </Link>
              <button className="btn bg-slate-800/80 backdrop-blur-sm hover:bg-slate-700 px-8 py-4 text-lg rounded-xl border border-slate-700/50 transition-all duration-300 hover:scale-105">
                Join the Waitlist
              </button>
            </motion.div>
          </div>
        </div>
      </motion.section>

      {/* Features Section */}
      <section id="features" className="py-24 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950" />
        <div className="container mx-auto px-4 relative">
          <div className="max-w-3xl mx-auto text-center mb-16">
            <h2 className="text-4xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
              Why TAO Galaxy
            </h2>
            <p className="text-lg text-slate-300 leading-relaxed">
              As Bittensor grows exponentially, navigating its ecosystem becomes increasingly complex. 
              TAO Galaxy provides the clarity, research tools, and user-friendly discovery platform 
              needed to understand and participate in the network effectively.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                icon: <Compass />,
                title: 'Subnet Explorer',
                description: 'Interactive visual map with powerful filters to discover and analyze subnets'
              },
              {
                icon: <FileText />,
                title: 'AI Reports',
                description: 'Detailed subnet analysis with scores based on deep subnet fundamentals analysis'
              },
              {
                icon: <RssIcon />,
                title: 'News Feed',
                description: 'Real-time updates and daily recaps from across the ecosystem'
              },
              {
                icon: <Bot />,
                title: 'MCP AI Assistant',
                description: 'Ask anything about Bittensor or any subnet and get structured, accurate answers'
              }
            ].map((feature, index) => (
              <motion.div 
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="group"
              >
                <div className="card p-6 hover:border-indigo-500/50 transition-all duration-300 hover:scale-105 bg-gradient-to-br from-slate-800/80 to-slate-900/80">
                  <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-indigo-500/20 to-purple-500/20 flex items-center justify-center text-indigo-400 mb-4 group-hover:scale-110 transition-transform duration-300">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold mb-3 bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-300">
                    {feature.title}
                  </h3>
                  <p className="text-slate-300">{feature.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Who Is TAO Galaxy For? Section */}
      <section id="about" className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-900/10 to-purple-900/10" />
        <div className="container mx-auto px-4 relative">
          <div className="max-w-3xl mx-auto text-center mb-16">
            <h2 className="text-4xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
              Who Is TAO Galaxy For?
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: <BarChart />,
                title: 'Investors & Analysts',
                subtitle: 'Discover, understand, and evaluate subnets—faster and with more confidence.',
                features: roleFeatures.investors
              },
              {
                icon: <Rocket />,
                title: 'Subnet Owners',
                subtitle: 'Show the world what you\'re building—and why it matters.',
                features: roleFeatures.owners
              },
              {
                icon: <Code />,
                title: 'Developers',
                subtitle: 'Find the best places to build, mine, or contribute.',
                features: roleFeatures.developers
              }
            ].map((role, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="group h-full"
              >
                <div className="card p-8 h-full hover:border-indigo-500/50 transition-all duration-300 hover:scale-105 bg-gradient-to-br from-slate-800/80 to-slate-900/80">
                  <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-indigo-500/20 to-purple-500/20 flex items-center justify-center text-indigo-400 mb-6 group-hover:scale-110 transition-transform duration-300">
                    {role.icon}
                  </div>
                  <h3 className="text-2xl font-semibold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-300">
                    {role.title}
                  </h3>
                  <p className="text-indigo-400 text-sm mb-6">{role.subtitle}</p>
                  <ul className="space-y-3">
                    {role.features.map((feature, fIndex) => (
                      <li key={fIndex} className="flex items-start gap-2 text-slate-300">
                        <div className="w-1.5 h-1.5 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 mt-2" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Quote Section */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-slate-900 via-slate-950 to-slate-900" />
        <div className="container mx-auto px-4 relative">
          <motion.blockquote 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="max-w-4xl mx-auto text-center"
          >
            <p className="text-3xl md:text-4xl font-medium text-slate-200 italic mb-8 leading-relaxed">
              "If we want to onboard the next wave into Bittensor, this is the tool that gets them there."
            </p>
            <footer className="text-slate-400">
              - Core Contributor
            </footer>
          </motion.blockquote>
        </div>
      </section>

      {/* Contact Form Section */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(99,102,241,0.1),transparent_70%)]" />
        <div className="container mx-auto px-4 relative">
          <div className="max-w-3xl mx-auto text-center mb-16">
            <h2 className="text-4xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
              Join the Future of AI
            </h2>
            <p className="text-lg text-slate-300 leading-relaxed">
              Be part of the next evolution in decentralized intelligence. 
              Sign up to get early access and exclusive updates.
            </p>
          </div>

          {/* Contact Form */}
          <div className="max-w-xl mx-auto">
            <div className="card p-8 bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-sm">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-slate-300 mb-2">
                    Name
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full bg-slate-800/50 border border-slate-700/50 rounded-lg px-4 py-3 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25 transition-all duration-200"
                    placeholder="Your name"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full bg-slate-800/50 border border-slate-700/50 rounded-lg px-4 py-3 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25 transition-all duration-200"
                    placeholder="your@email.com"
                  />
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-slate-300 mb-2">
                    Message
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    rows={4}
                    className="w-full bg-slate-800/50 border border-slate-700/50 rounded-lg px-4 py-3 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25 transition-all duration-200"
                    placeholder="Tell us about yourself and your interest in TAO Galaxy"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full btn py-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 rounded-xl shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:scale-105"
                >
                  Get Early Access
                </button>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-slate-800 relative">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-2">
              <Zap className="text-indigo-500" size={24} />
              <span className="text-xl font-semibold bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-purple-500">
                TAO Galaxy
              </span>
            </div>
            
            <div className="flex items-center gap-6">
              <a href="#" className="text-slate-400 hover:text-white transition-all duration-200 hover:scale-110">
                <Twitter size={20} />
              </a>
              <a href="#" className="text-slate-400 hover:text-white transition-all duration-200 hover:scale-110">
                <Github size={20} />
              </a>
            </div>

            <div className="flex items-center gap-6 text-sm">
              <a href="#" className="text-slate-400 hover:text-white transition-colors">Terms</a>
              <a href="#" className="text-slate-400 hover:text-white transition-colors">Privacy</a>
              <a href="#" className="text-slate-400 hover:text-white transition-colors">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;