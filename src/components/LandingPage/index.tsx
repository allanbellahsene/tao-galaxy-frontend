import React, { useState, ChangeEvent, FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Zap, ArrowRight, Compass, FileText, RssIcon, Bot, Users, ArrowUpRight, Github, Twitter, LineChart, Code, Search, BookOpen, BarChart, Rocket, Brain } from 'lucide-react';
import { fadeIn, staggerContainer } from './animations';

interface FormData {
  name: string;
  email: string;
  message: string;
}

interface Feature {
  icon: React.ReactNode;
  title: string;
  description: string;
  image: string;
  details: string[];
}

interface RoleFeature {
  icon: React.ReactNode;
  title: string;
  subtitle: string;
  features: string[];
}

const LandingPage: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    message: ''
  });

  const [activeFeature, setActiveFeature] = useState(0);
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);
  const [previewImage, setPreviewImage] = useState<string | null>(null);

  const features: Feature[] = [
    {
      icon: <Compass />,
      title: 'Subnet Explorer',
      description: 'Interactive visual map with powerful filters to discover and analyze subnets',
      image: '/screenshots/subnet-explorer.png',
      details: []
    },
    {
      icon: <FileText />,
      title: 'AI Reports',
      description: 'Detailed subnet analysis with scores based on deep subnet fundamentals analysis',
      image: '/screenshots/ai-reports.png',
      details: [
        'Comprehensive subnet analysis',
        'Performance metrics tracking',
        'Risk assessment scores',
        'Historical data analysis'
      ]
    },
    {
      icon: <RssIcon />,
      title: 'News Feed',
      description: 'Real-time updates and daily recaps from across the ecosystem',
      image: '/screenshots/news-feature.png',
      details: []
    },
    {
      icon: <Bot />,
      title: 'MCP AI Assistant',
      description: 'Ask anything about Bittensor or any subnet and get structured, accurate answers',
      image: '/screenshots/ai-assistant.png',
      details: [
        'Natural language queries',
        'Context-aware responses',
        'Technical documentation',
        'Integration guides'
      ]
    }
  ];

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    setFormData({ name: '', email: '', message: '' });
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData((prev: FormData) => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const roleFeatures: RoleFeature[] = [
    {
      icon: <BarChart />,
      title: 'Investors & Analysts',
      subtitle: 'Discover, understand, and evaluate subnets—faster and with more confidence.',
      features: [
        'Explore new opportunities visually',
        'Compare teams, traction, and transparency with AI-driven scores',
        'Stay ahead with real-time ecosystem updates',
        'Make smarter, faster allocation decisions'
      ]
    },
    {
      icon: <Rocket />,
      title: 'Subnet Owners',
      subtitle: 'Show the world what you\'re building—and why it matters.',
      features: [
        'Showcase your team, product, and progress',
        'Attract investors, miners, and collaborators',
        'Let your growth speak for itself through verified reports and news',
        'Build stronger community engagement'
      ]
    },
    {
      icon: <Code />,
      title: 'Developers',
      subtitle: 'Find the best places to build, mine, or contribute.',
      features: [
        'Discover subnets with real traction',
        'Track launches and activity spikes',
        'Identify collaboration or reward opportunities with clarity',
        'Access comprehensive development resources'
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-sm border-b border-slate-800">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Zap className="text-indigo-500" size={24} />
              <span className="text-xl font-semibold bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-purple-500">TAO Galaxy</span>
            </div>
            <div className="hidden md:flex items-center gap-6">
              <a href="#features" className="text-sm text-slate-300 hover:text-white transition-colors">Features</a>
              <a href="#about" className="text-sm text-slate-300 hover:text-white transition-colors">About</a>
              <Link to="/app" className="btn btn-primary bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500">
                Launch App
              </Link>
            </div>
            <Link to="/app" className="md:hidden btn btn-primary bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500">
              Launch
            </Link>
          </div>
        </div>
      </nav>

      <motion.section 
        variants={staggerContainer}
        initial="hidden"
        animate="show"
        className="min-h-screen flex items-center justify-center pt-16 relative overflow-hidden"
      >
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(99,102,241,0.15),transparent_50%)]" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] md:w-[800px] h-[400px] md:h-[800px] rounded-full border border-indigo-500/10 animate-[spin_60s_linear_infinite]" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[300px] md:w-[600px] h-[300px] md:h-[600px] rounded-full border border-purple-500/10 animate-[spin_40s_linear_infinite_reverse]" />
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
              className="text-4xl md:text-7xl font-bold mb-6 md:mb-8 bg-clip-text text-transparent bg-gradient-to-r from-white via-indigo-200 to-purple-300 leading-tight"
            >
              The Intelligence Layer of Bittensor
            </motion.h1>
            
            <motion.p 
              variants={fadeIn}
              className="text-lg md:text-xl text-slate-300 mb-8 md:mb-12 max-w-2xl mx-auto leading-relaxed"
            >
              Discover, evaluate, and stay updated on everything happening across the subnet galaxy.
            </motion.p>
            
            <motion.div variants={fadeIn} className="flex flex-col md:flex-row items-center justify-center gap-4">
              <Link 
                to="/app" 
                className="w-full md:w-auto btn px-8 py-4 text-lg bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 rounded-xl shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:scale-105"
              >
                Explore the Galaxy
              </Link>
              <button className="w-full md:w-auto btn bg-slate-800/80 backdrop-blur-sm hover:bg-slate-700 px-8 py-4 text-lg rounded-xl border border-slate-700/50 transition-all duration-300 hover:scale-105">
                Join the Waitlist
              </button>
            </motion.div>
          </div>
        </div>
      </motion.section>

      <section id="features" className="py-16 md:py-24 relative overflow-hidden">
        <div className="container mx-auto px-4 relative">
          <div className="max-w-3xl mx-auto text-center mb-12 md:mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
              Powerful Features for the Bittensor Ecosystem
            </h2>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 md:gap-12 items-center">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {features.map((feature, index) => (
                <motion.div 
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className={`group cursor-pointer ${activeFeature === index ? 'ring-2 ring-indigo-500' : ''}`}
                  onClick={() => setActiveFeature(index)}
                >
                  <div className="card p-4 md:p-6 hover:border-indigo-500/50 transition-all duration-300 hover:scale-105 bg-gradient-to-br from-slate-800/80 to-slate-900/80 h-full">
                    <div className="w-10 h-10 md:w-12 md:h-12 rounded-lg bg-gradient-to-br from-indigo-500/20 to-purple-500/20 flex items-center justify-center text-indigo-400 mb-3 md:mb-4 group-hover:scale-110 transition-transform duration-300">
                      {feature.icon}
                    </div>
                    <h3 className="text-lg md:text-xl font-semibold mb-2 md:mb-3 bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-300">
                      {feature.title}
                    </h3>
                    <p className="text-slate-300 text-sm">{feature.description}</p>
                  </div>
                </motion.div>
              ))}
            </div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="relative flex items-center justify-center mt-8 md:mt-0"
            >
              <div className="w-full max-w-2xl mx-auto bg-slate-900 rounded-3xl shadow-2xl border-2 border-slate-800 overflow-hidden flex flex-col" style={{ minHeight: 280 }}>
                <div className="flex items-center px-4 md:px-6 py-3 bg-slate-800 border-b border-slate-700" style={{ minHeight: 48 }}>
                  <span className="w-3 h-3 bg-red-400 rounded-full mr-2"></span>
                  <span className="w-3 h-3 bg-yellow-400 rounded-full mr-2"></span>
                  <span className="w-3 h-3 bg-green-400 rounded-full"></span>
                  <span className="ml-4 md:ml-6 text-sm text-slate-400 font-mono truncate" style={{ maxWidth: 220 }}>
                    {features[activeFeature].title}
                  </span>
                </div>
                <div
                  className="flex-1 bg-slate-950 flex items-center justify-center cursor-zoom-in"
                  onClick={() => {
                    setPreviewImage(features[activeFeature].image);
                    setIsPreviewOpen(true);
                  }}
                >
                  <img
                    src={features[activeFeature].image}
                    alt={features[activeFeature].title}
                    className="w-full h-full object-cover rounded-b-3xl transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-2xl"
                    style={{ minHeight: 180, maxHeight: 360 }}
                  />
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      <section id="about" className="py-16 md:py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-900/10 to-purple-900/10" />
        <div className="container mx-auto px-4 relative">
          <div className="max-w-3xl mx-auto text-center mb-12 md:mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
              Who Is TAO Galaxy For?
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
            {roleFeatures.map((role, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="group h-full"
              >
                <div className="card p-6 md:p-8 h-full hover:border-indigo-500/50 transition-all duration-300 hover:scale-105 bg-gradient-to-br from-slate-800/80 to-slate-900/80">
                  <div className="w-12 h-12 md:w-14 md:h-14 rounded-lg bg-gradient-to-br from-indigo-500/20 to-purple-500/20 flex items-center justify-center text-indigo-400 mb-4 md:mb-6 group-hover:scale-110 transition-transform duration-300">
                    {role.icon}
                  </div>
                  <h3 className="text-xl md:text-2xl font-semibold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-300">
                    {role.title}
                  </h3>
                  <p className="text-indigo-400 text-sm mb-4 md:mb-6">{role.subtitle}</p>
                  <ul className="space-y-2 md:space-y-3">
                    {role.features.map((feature, fIndex) => (
                      <li key={fIndex} className="flex items-start gap-2 text-slate-300 text-sm md:text-base">
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

      <section className="py-16 md:py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(99,102,241,0.1),transparent_70%)]" />
        <div className="container mx-auto px-4 relative">
          <div className="max-w-3xl mx-auto text-center mb-12 md:mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
              Join the Future of AI
            </h2>
            <p className="text-base md:text-lg text-slate-300 leading-relaxed">
              Be part of the next evolution in decentralized intelligence. 
              Sign up to get early access and exclusive updates.
            </p>
          </div>

          <div className="max-w-xl mx-auto">
            <div className="card p-6 md:p-8 bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-sm">
              <form onSubmit={handleSubmit} className="space-y-4 md:space-y-6">
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
                  className="w-full btn py-3 md:py-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 rounded-xl shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:scale-105"
                >
                  Get Early Access
                </button>
              </form>
            </div>
          </div>
        </div>
      </section>

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
              - Allan, Founder of TAO Galaxy
            </footer>
          </motion.blockquote>
        </div>
      </section>

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

      {/* Modal/Lightbox for screenshot preview */}
      {isPreviewOpen && previewImage && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/80"
          onClick={() => setIsPreviewOpen(false)}
        >
          <img
            src={previewImage}
            alt="Preview"
            className="max-w-3xl max-h-[90vh] rounded-2xl shadow-2xl border-4 border-slate-800"
            onClick={e => e.stopPropagation()}
          />
          <button
            className="absolute top-8 right-8 text-white text-3xl font-bold"
            onClick={() => setIsPreviewOpen(false)}
          >
            &times;
          </button>
        </div>
      )}
    </div>
  );
};

export default LandingPage;