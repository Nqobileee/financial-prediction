# Project Structure Documentation

## Overview

FinHealth is a Next.js 15 application implementing a financial health prediction system for Small and Medium Enterprises (SMEs) across Southern Africa. The project employs modern web development practices with TypeScript for type safety and Tailwind CSS for responsive design.

## Architecture

```
financial-prediction/
├── .env.local                  # Environment configuration (local development)
├── .env.production            # Production environment variables
├── .gitignore                 # Git ignore patterns
├── next.config.mjs            # Next.js configuration
├── next-env.d.ts             # Next.js TypeScript declarations
├── package.json               # Node.js dependencies and scripts
├── package-lock.json          # Locked dependency versions
├── postcss.config.mjs         # PostCSS configuration for Tailwind
├── tailwind.config.ts         # Tailwind CSS configuration
├── tsconfig.json              # TypeScript compiler configuration
├── vercel.json                # Vercel deployment configuration
├── README.md                  # Project documentation and research overview
├── CITATIONS.md               # Data attribution and licensing information
├── PROJECT_STRUCTURE.md       # This file - comprehensive project documentation
└── src/                       # Source code directory
    ├── app/                   # Next.js App Router directory
    │   ├── globals.css        # Global CSS styles and Tailwind imports
    │   ├── layout.tsx         # Root layout component
    │   ├── page.tsx           # Home page component
    │   ├── api/               # Next.js API Routes (Backend)
    │   │   ├── health/        # Health check endpoint
    │   │   │   └── route.ts   # GET /api/health - API status verification
    │   │   └── predict/       # Prediction endpoint
    │   │       └── route.ts   # POST /api/predict - Financial health assessment
    │   ├── reports/           # Reports and results pages
    │   │   └── page.tsx       # Prediction results display
    │   ├── results/           # Alternative results page
    │   │   └── page.tsx       # Results visualization
    │   └── survey/            # Survey module
    │       ├── layout.tsx     # Survey-specific layout
    │       └── page.tsx       # Financial health survey form
    ├── components/            # Reusable React components
    │   ├── ApiStatus.tsx      # API connection status indicator
    │   ├── Footer.tsx         # Application footer component
    │   └── Navbar.tsx         # Navigation bar component
    └── lib/                   # Utility libraries and configurations
        └── api.ts             # API client utilities and type definitions
```

## Directory Structure Details

### Root Configuration Files

**Environment Configuration:**
- `.env.local` - Local development environment variables
- `.env.production` - Production deployment environment settings

**Build Configuration:**
- `next.config.mjs` - Next.js framework configuration
- `tailwind.config.ts` - Tailwind CSS utility classes and design system
- `postcss.config.mjs` - CSS processing pipeline configuration
- `tsconfig.json` - TypeScript compilation settings and path mappings

**Deployment Configuration:**
- `vercel.json` - Vercel platform deployment settings
- `package.json` - Node.js dependencies, scripts, and metadata

### Source Code Organization (`src/`)

#### Application Pages (`src/app/`)

**Core Pages:**
- `layout.tsx` - Root application layout defining global structure
- `page.tsx` - Landing page with application overview and navigation

**Feature Pages:**
- `survey/page.tsx` - Interactive 16-question financial health assessment form
- `reports/page.tsx` - Comprehensive prediction results with confidence scores
- `results/page.tsx` - Alternative results visualization interface

#### API Routes (`src/app/api/`)

**Health Monitoring:**
- `health/route.ts` - System health check endpoint
  - `GET /api/health` - Returns API status and availability

**Prediction Engine:**
- `predict/route.ts` - Financial health assessment endpoint
  - `POST /api/predict` - Processes survey data and returns risk classification

#### Reusable Components (`src/components/`)

**Navigation Components:**
- `Navbar.tsx` - Primary navigation with responsive design
- `Footer.tsx` - Application footer with attribution and links

**Status Components:**
- `ApiStatus.tsx` - Real-time API connectivity indicator

#### Utility Libraries (`src/lib/`)

**API Management:**
- `api.ts` - Centralized API client with type definitions
  - Request/response type interfaces
  - Error handling utilities
  - Environment-based URL configuration

## Technology Stack

### Frontend Framework
- **Next.js 15** - React framework with App Router
- **React 18** - Component-based UI library
- **TypeScript 5.0+** - Static type checking and enhanced IDE support

### Styling and Design
- **Tailwind CSS** - Utility-first CSS framework
- **PostCSS** - CSS processing and optimization
- **Responsive Design** - Mobile-first approach with breakpoint utilities

### Backend Implementation
- **Next.js API Routes** - Server-side API endpoints
- **TypeScript** - Type-safe server logic
- **Financial Scoring Algorithm** - Custom heuristic-based risk assessment

### Development Tools
- **ESLint** - Code quality and consistency
- **Prettier** - Code formatting
- **Git** - Version control

## Data Flow Architecture

### Request Processing Pipeline

1. **User Input Collection** (`survey/page.tsx`)
   - Form validation and sanitization
   - Client-side data formatting
   - Progress tracking and user experience optimization

2. **API Request Transmission** (`lib/api.ts`)
   - HTTP request configuration
   - Error handling and retry logic
   - Response type validation

3. **Server-Side Processing** (`api/predict/route.ts`)
   - Input validation and sanitization
   - Financial health score calculation
   - Risk categorization algorithm
   - Confidence score generation

4. **Response Delivery** (`reports/page.tsx`)
   - Results visualization
   - Recommendation generation
   - Export and sharing capabilities

### Financial Health Assessment Algorithm

**Scoring Methodology:**
The TypeScript-based scoring system employs weighted factor analysis:

1. **Income Stability Assessment (40% weight)**
   - Business turnover to expense ratio analysis
   - Cash flow pattern evaluation

2. **Financial Management Practices (25% weight)**
   - Record-keeping quality assessment
   - Insurance coverage analysis

3. **Technology Adoption Indicators (15% weight)**
   - Mobile money integration
   - Digital payment platform usage

4. **Business Resilience Factors (10% weight)**
   - COVID-19 essential service classification
   - Market stability perception

5. **Compliance and Planning (10% weight)**
   - Tax compliance history
   - Growth motivation assessment

## Development Workflow

### Local Development Setup

```bash
# Environment initialization
npm install                    # Install dependencies
npm run dev                   # Start development server
npm run build                 # Production build
npm run start                 # Production server
npm run lint                  # Code quality check
```

### File Organization Conventions

**Naming Conventions:**
- Components: PascalCase (`ApiStatus.tsx`)
- Pages: lowercase with extensions (`page.tsx`)
- Utilities: camelCase (`api.ts`)
- Constants: UPPER_SNAKE_CASE

**Import Organization:**
- External libraries first
- Internal utilities second
- Component imports third
- Type-only imports last

### Code Quality Standards

**TypeScript Configuration:**
- Strict mode enabled for enhanced type safety
- Path mapping for clean import statements
- ESNext target for modern JavaScript features

**Component Structure:**
- Functional components with hooks
- TypeScript interfaces for props
- Consistent error handling patterns

## API Documentation

### Endpoint Specifications

#### Health Check Endpoint
```typescript
GET /api/health
Response: {
  success: boolean;
  message: string;
  status: string;
  model_trained: boolean;
  timestamp: string;
}
```

#### Prediction Endpoint
```typescript
POST /api/predict
Request: {
  country: string;
  owner_age: number;
  personal_income: number;
  business_turnover: number;
  // ... additional survey fields
}

Response: {
  success: boolean;
  prediction: 'Low' | 'Medium' | 'High';
  confidence_scores: {
    Low: number;
    Medium: number;
    High: number;
  };
  recommendation: string;
  survey_data: SurveyData;
}
```

## Deployment Architecture

### Environment Configuration
- **Development**: Local Next.js server with hot reloading
- **Production**: Vercel platform with global CDN distribution
- **API Routes**: Server-side rendering with automatic optimization

### Performance Optimization
- **Static Site Generation** for content pages
- **Server-Side Rendering** for dynamic prediction results
- **Image Optimization** through Next.js built-in capabilities
- **CSS Optimization** via Tailwind's purge functionality

## Security Considerations

### Data Protection
- Client-side input validation and sanitization
- Server-side request validation
- No persistent storage of sensitive survey data
- HTTPS enforcement for all communications

### API Security
- Rate limiting through Vercel edge functions
- CORS configuration for controlled access
- Input validation for SQL injection prevention
- Error handling without sensitive information exposure

## Future Development Roadmap

### Planned Enhancements
- **Multi-language Support** for regional accessibility
- **Advanced Analytics Dashboard** for trend analysis
- **Export Functionality** for PDF report generation
- **Integration APIs** for external financial systems

### Scalability Considerations
- **Database Integration** for historical data analysis
- **Caching Layer** implementation for improved performance
- **Microservices Architecture** for feature isolation
- **Machine Learning Pipeline** integration for enhanced predictions

## Maintenance and Support

### Monitoring and Logging
- Vercel Analytics for performance tracking
- Error boundary implementation for graceful failure handling
- Health check endpoints for system status monitoring

### Version Control and Deployment
- Git-based version control with semantic versioning
- Continuous deployment through Vercel GitHub integration
- Automated testing pipeline for quality assurance

This documentation provides a comprehensive overview of the FinHealth project structure, enabling developers to understand the codebase architecture, data flow, and implementation patterns used throughout the application.