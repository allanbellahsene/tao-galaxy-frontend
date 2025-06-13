// generate-all-reports.js
const fs = require('fs');
const path = require('path');
const Handlebars = require('handlebars');

class SubnetReportGenerator {
  constructor() {
    this.dataDir = './data';
    this.templateDir = './templates';
    this.outputDir = './output';
    this.template = null;
  }

  // Initialize templates and helpers
  async init() {
    // Load main template
    const templateSource = fs.readFileSync(
      path.join(this.templateDir, 'subnet-report.hbs'), 
      'utf8'
    );
    this.template = Handlebars.compile(templateSource);

    // Register partials
    this.registerPartials();
    
    // Register custom helpers
    this.registerHelpers();
  }

  registerPartials() {
    const partialsDir = path.join(this.templateDir, 'partials');
    const partialFiles = fs.readdirSync(partialsDir);
    
    partialFiles.forEach(file => {
      if (file.endsWith('.hbs')) {
        const partialName = path.basename(file, '.hbs');
        const partialContent = fs.readFileSync(
          path.join(partialsDir, file), 
          'utf8'
        );
        Handlebars.registerPartial(partialName, partialContent);
        console.log(`✓ Registered partial: ${partialName}`);
      }
    });
  }

  registerHelpers() {
    // Helper to extract numerical rating
    Handlebars.registerHelper('extractRating', (ratingString) => {
      const match = ratingString.match(/\((\d+)\/5\)/);
      return match ? parseInt(match[1]) : 3;
    });

    // Helper to extract rating text
    Handlebars.registerHelper('extractRatingText', (ratingString) => {
      return ratingString.split('(')[0].trim();
    });

    // Helper to convert percentile to number
    Handlebars.registerHelper('percentileToNumber', (percentileString) => {
      if (percentileString.includes("Top 10%")) return 90;
      if (percentileString.includes("Top 25%")) return 75;
      if (percentileString.includes("Top 50%")) return 50;
      if (percentileString.includes("Bottom 50%")) return 25;
      if (percentileString.includes("Bottom 25%")) return 10;
      return 50;
    });

    // Helper for risk level colors
    Handlebars.registerHelper('riskColor', (riskLevel) => {
      if (riskLevel.includes('Low')) return 'green';
      if (riskLevel.includes('Medium')) return 'orange';
      if (riskLevel.includes('High')) return 'red';
      if (riskLevel.includes('Very High')) return 'darkred';
      return 'gray';
    });

    // Helper for investment rating colors
    Handlebars.registerHelper('investmentColor', (rating) => {
      if (rating.includes('Strong Buy')) return 'darkgreen';
      if (rating.includes('Buy')) return 'green';
      if (rating.includes('Hold')) return 'orange';
      if (rating.includes('Sell')) return 'red';
      return 'gray';
    });
  }

  // Find all subnet IDs from research files
  getSubnetIds() {
    const researchDir = path.join(this.dataDir, 'research');
    const files = fs.readdirSync(researchDir);
    
    return files
      .filter(file => file.endsWith('_research.json'))
      .map(file => file.replace('_research.json', ''))
      .sort((a, b) => {
        // Sort numerically (SN1, SN2, ..., SN64, etc.)
        const numA = parseInt(a.replace('SN', ''));
        const numB = parseInt(b.replace('SN', ''));
        return numA - numB;
      });
  }

  // Load and merge data for a specific subnet
  loadSubnetData(subnetId) {
    const researchPath = path.join(
      this.dataDir, 
      'research', 
      `${subnetId}_research.json`
    );
    const analysisPath = path.join(
      this.dataDir, 
      'analysis', 
      `${subnetId}_analysis.json`
    );

    let researchData = {};
    let analysisData = {};

    // Load research data
    if (fs.existsSync(researchPath)) {
      researchData = JSON.parse(fs.readFileSync(researchPath, 'utf8'));
    } else {
      console.warn(`Research data not found for ${subnetId}`);
    }

    // Load analysis data
    if (fs.existsSync(analysisPath)) {
      analysisData = JSON.parse(fs.readFileSync(analysisPath, 'utf8'));
    } else {
      console.warn(`Analysis data not found for ${subnetId}`);
    }

    // Merge and enrich data
    return this.enrichSubnetData({
      subnetId,
      research: researchData,
      analysis: analysisData
    });
  }

  // Enrich data with computed values for templates
  enrichSubnetData(data) {
    const enriched = { ...data };

    // Basic Information
    enriched.basicInfo = {
      name: data.research?.I_BASIC_SUBNET_INFORMATION?.Subnet_Name || 'Unknown',
      id: data.research?.I_BASIC_SUBNET_INFORMATION?.Subnet_ID || data.subnetId,
      mission: data.research?.I_BASIC_SUBNET_INFORMATION?.Subnet_Mission_One_Sentence || 'No mission statement available'
    };

    // Team Information
    enriched.teamInfo = {
      isDoxxed: data.research?.II_TEAM?.Team_Doxxed === 'Yes',
      foundingTeam: this.parseTeamMembers(data.research?.II_TEAM?.Founding_Team),
      teamBackground: data.research?.II_TEAM?.Founding_Team_Background,
      affiliatedOrgs: data.research?.II_TEAM?.Affiliated_Organizations
    };

    // Problem & Market Analysis
    enriched.problemAnalysis = {
      mission: data.research?.III_PROBLEM_SOLVING?.Mission,
      realWorldProblem: data.research?.III_PROBLEM_SOLVING?.Real_World_Problem,
      problemDescription: data.research?.III_PROBLEM_SOLVING?.Problem_Description,
      tam: data.research?.III_PROBLEM_SOLVING?.Estimated_TAM,
      pathToAdoption: data.research?.III_PROBLEM_SOLVING?.Path_to_Mass_Adoption,
      keyChallenges: this.parseList(data.research?.III_PROBLEM_SOLVING?.Key_Challenges),
      competitors: this.parseList(data.research?.III_PROBLEM_SOLVING?.Main_Competitors_Non_Web3),
      competitiveAdvantage: data.research?.III_PROBLEM_SOLVING?.Competitive_Advantage,
      subnetNecessity: data.research?.III_PROBLEM_SOLVING?.Subnet_Necessity,
      visionDifference: data.research?.III_PROBLEM_SOLVING?.Vision_Difference
    };

    // Market Opportunity Analysis
    enriched.marketAnalysis = {
      sizeAssessment: data.analysis?.II_MARKET_OPPORTUNITY?.Market_Size_Assessment,
      timingAssessment: data.analysis?.II_MARKET_OPPORTUNITY?.Market_Timing_Assessment,
      competitivePosition: data.analysis?.II_MARKET_OPPORTUNITY?.Competitive_Position_Strength,
      moatAssessment: data.analysis?.II_MARKET_OPPORTUNITY?.Moat_Assessment
    };

    // Product & Development
    enriched.productInfo = {
      revenueStreams: data.research?.IV_REVENUE_PRODUCT?.Products_Revenue_Streams,
      monetizationPath: data.research?.IV_REVENUE_PRODUCT?.Path_to_Monetization,
      developmentPhase: data.research?.IV_REVENUE_PRODUCT?.Product_Development_Phase,
      hasRevenue: data.research?.IV_REVENUE_PRODUCT?.Product_Generating_Revenue === 'Yes',
      lifecyclePhase: data.research?.IV_REVENUE_PRODUCT?.Product_Lifecycle_Phase
    };

    enriched.developmentInfo = {
      isOpenSource: data.research?.VI_DEVELOPMENT?.Codebase_Open_Source === 'Yes',
      repoLink: data.research?.VI_DEVELOPMENT?.Main_Repository_Link,
      updateActivity: data.research?.VI_DEVELOPMENT?.Recent_Update_Activity,
      activeContributors: data.research?.VI_DEVELOPMENT?.Active_Contributors_Last_3_Months,
      hasProfessionalPractices: data.research?.VI_DEVELOPMENT?.Professional_Development_Practices === 'Yes',
      hasTechnicalRoadmap: data.research?.VI_DEVELOPMENT?.Technical_Roadmap_Published === 'Yes',
      hasTechnicalDocs: data.research?.VI_DEVELOPMENT?.Technical_Documents_Status,
      recentFeatures: this.parseList(data.research?.VI_DEVELOPMENT?.Recent_Feature_Releases),
      thirdPartyActivity: data.research?.VI_DEVELOPMENT?.Third_Party_Developer_Activity
    };

    // Marketing & Community
    enriched.marketingInfo = {
      channels: this.parseList(data.research?.V_MARKETING?.Main_Communication_Channels),
      frequency: data.research?.V_MARKETING?.Communication_Frequency,
      effort: data.research?.V_MARKETING?.Communication_Effort,
      communityResponsiveness: data.research?.V_MARKETING?.Community_Responsiveness
    };

    // Investment Analysis
    enriched.investmentInfo = {
      rating: this.extractRating(data.analysis?.I_INVESTMENT_THESIS?.Overall_Investment_Rating),
      ratingText: this.extractRatingText(data.analysis?.I_INVESTMENT_THESIS?.Overall_Investment_Rating),
      thesis: data.analysis?.I_INVESTMENT_THESIS?.Investment_Thesis_Summary,
      strengths: this.parseList(data.analysis?.I_INVESTMENT_THESIS?.Key_Investment_Strengths),
      risks: this.parseList(data.analysis?.I_INVESTMENT_THESIS?.Key_Investment_Risks)
    };

    // Financial Viability
    enriched.financialInfo = {
      revenuePotential: data.analysis?.IV_FINANCIAL_VIABILITY?.Revenue_Potential_Assessment,
      monetizationClarity: data.analysis?.IV_FINANCIAL_VIABILITY?.Monetization_Clarity_Rating,
      sustainability: data.analysis?.IV_FINANCIAL_VIABILITY?.Business_Model_Sustainability,
      marketFit: data.analysis?.IV_FINANCIAL_VIABILITY?.Product_Market_Fit_Stage
    };

    // Risk Assessment
    enriched.riskData = [
      { type: 'Technical', level: data.analysis?.V_RISK_ASSESSMENT?.Technical_Risk_Level },
      { type: 'Market', level: data.analysis?.V_RISK_ASSESSMENT?.Market_Risk_Level },
      { type: 'Team', level: data.analysis?.V_RISK_ASSESSMENT?.Team_Risk_Level },
      { type: 'Regulatory', level: data.analysis?.V_RISK_ASSESSMENT?.Regulatory_Risk_Level },
      { type: 'Competition', level: data.analysis?.V_RISK_ASSESSMENT?.Competition_Risk_Level }
    ];

    // Comparative Metrics
    enriched.percentileData = [
      {
        metric: 'Development',
        value: this.percentileToNumber(data.analysis?.VI_COMPARATIVE_METRICS?.Development_Activity_Percentile)
      },
      {
        metric: 'Team Quality',
        value: this.percentileToNumber(data.analysis?.VI_COMPARATIVE_METRICS?.Team_Quality_Percentile)
      },
      {
        metric: 'Market Opportunity',
        value: this.percentileToNumber(data.analysis?.VI_COMPARATIVE_METRICS?.Market_Opportunity_Percentile)
      },
      {
        metric: 'Innovation',
        value: this.percentileToNumber(data.analysis?.VI_COMPARATIVE_METRICS?.Innovation_Level_Percentile)
      }
    ];

    // Investment Recommendation
    enriched.recommendation = {
      allocation: data.analysis?.VII_INVESTMENT_RECOMMENDATION?.Recommended_Allocation_Percentage,
      timeline: data.analysis?.VII_INVESTMENT_RECOMMENDATION?.Investment_Timeline,
      milestones: this.parseList(data.analysis?.VII_INVESTMENT_RECOMMENDATION?.Key_Milestones_to_Watch),
      exitTriggers: this.parseList(data.analysis?.VII_INVESTMENT_RECOMMENDATION?.Exit_Triggers)
    };

    return enriched;
  }

  // Helper methods for data processing
  parseTeamMembers(teamString) {
    if (!teamString) return [];
    return teamString.split(',').map(member => member.trim());
  }

  parseList(listString) {
    if (!listString) return [];
    if (Array.isArray(listString)) return listString;
    return listString.split(',').map(item => item.trim());
  }

  extractRating(ratingString) {
    if (!ratingString) return 3;
    const match = ratingString.match(/\((\d+)\/5\)/);
    return match ? parseInt(match[1]) : 3;
  }

  extractRatingText(ratingString) {
    if (!ratingString) return 'Not Rated';
    return ratingString.split('(')[0].trim();
  }

  percentileToNumber(percentileString) {
    if (!percentileString) return 50;
    if (percentileString.includes("Top 10%")) return 90;
    if (percentileString.includes("Top 25%")) return 75;
    if (percentileString.includes("Top 50%")) return 50;
    if (percentileString.includes("Bottom 50%")) return 25;
    if (percentileString.includes("Bottom 25%")) return 10;
    return 50;
  }

  // Generate single subnet report
  generateSubnetReport(subnetId) {
    console.log(`Generating report for ${subnetId}...`);
    
    const data = this.loadSubnetData(subnetId);
    const html = this.template(data);
    
    const outputPath = path.join(this.outputDir, 'reports', `${subnetId}.html`);
    fs.writeFileSync(outputPath, html);
    
    console.log(`✓ Generated ${subnetId}.html`);
    return data;
  }

  // Generate index page with all subnets
  generateIndexPage(allSubnetData) {
    const indexTemplate = Handlebars.compile(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>TAO Galaxy - Subnet Reports</title>
        <link rel="stylesheet" href="assets/report.css">
      </head>
      <body>
        <div class="container">
          <h1>TAO Galaxy Subnet Reports</h1>
          <div class="subnet-grid">
            {{#each subnets}}
            <div class="subnet-card">
              <h3><a href="reports/{{subnetId}}.html">{{subnetName}} ({{subnetId}})</a></h3>
              <p class="rating rating-{{overallRating}}">{{overallRatingText}}</p>
              <p>{{research.I_BASIC_SUBNET_INFORMATION.Subnet_Mission_One_Sentence}}</p>
            </div>
            {{/each}}
          </div>
        </div>
      </body>
      </html>
    `);

    const html = indexTemplate({ subnets: allSubnetData });
    const indexPath = path.join(this.outputDir, 'index.html');
    fs.writeFileSync(indexPath, html);
    
    console.log('✓ Generated index.html');
  }

  // Copy CSS assets
  copyAssets() {
    const assetsDir = path.join(this.outputDir, 'assets');
    if (!fs.existsSync(assetsDir)) {
      fs.mkdirSync(assetsDir, { recursive: true });
    }

    const cssSource = path.join(this.templateDir, 'styles', 'report.css');
    const cssTarget = path.join(assetsDir, 'report.css');
    
    if (fs.existsSync(cssSource)) {
      fs.copyFileSync(cssSource, cssTarget);
      console.log('✓ Copied CSS assets');
    }
  }

  // Main execution function
  async generateAllReports() {
    console.log('🚀 Starting TAO Galaxy Report Generation...\n');

    // Initialize
    await this.init();

    // Ensure output directories exist
    const reportsDir = path.join(this.outputDir, 'reports');
    if (!fs.existsSync(reportsDir)) {
      fs.mkdirSync(reportsDir, { recursive: true });
    }

    // Get all subnet IDs
    const subnetIds = this.getSubnetIds();
    console.log(`Found ${subnetIds.length} subnets: ${subnetIds.join(', ')}\n`);

    // Generate individual reports
    const allSubnetData = [];
    for (const subnetId of subnetIds) {
      try {
        const data = this.generateSubnetReport(subnetId);
        allSubnetData.push(data);
      } catch (error) {
        console.error(`❌ Error generating ${subnetId}:`, error.message);
      }
    }

    // Generate index page
    this.generateIndexPage(allSubnetData);

    // Copy assets
    this.copyAssets();

    console.log(`\n🎉 Generated ${allSubnetData.length} subnet reports successfully!`);
    console.log(`📁 Reports available in: ${this.outputDir}`);
  }
}

// CLI execution
if (require.main === module) {
  const generator = new SubnetReportGenerator();
  generator.generateAllReports().catch(console.error);
}

module.exports = SubnetReportGenerator;