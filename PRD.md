# Product Requirement Document (PRD): ViralWell

**Project Codename**: ViralWell  
**Version**: 1.0.0  
**Status**: Approved / In Development  

---

## 1. Executive Summary
ViralWell is a predictive data science analytics dashboard designed to model climate-health correlations, forecast regional epidemiological outbreak risks, and offer conversational wellness guidance. By integrating environmental telemetry (temperature, humidity, air quality index, and delayed rainfall indicators) with clinical risk models, ViralWell serves as an analytical simulation environment for researchers, healthcare administrators, and public health educators.

### 1.1 Objectives
*   **Simulate Epidemic Risk**: Provide real-time risk index calculations for vector-borne (Dengue, Malaria), water-borne (Gastroenteritis), climate-driven (Heatstroke), and respiratory diseases (Influenza, Bronchitis).
*   **Empower Public Health Decisions**: Facilitate regional planning through an interactive dashboard to visualize trends and log simulated forecasting runs.
*   **Bridge Analytics with Holism**: Offer holistic, botanical, and Ayurvedic recommendations alongside machine learning predictions using generative AI.

---

## 2. Core Features & Functional Requirements

### 2.1 Tab 1: Outbreak Predictor (Interactive Simulation Engine)
Allows users to input climate metrics manually or select preset scenarios to calculate immediate disease risk indicators.
*   **Location Coordinates**: Dynamic slider input for Latitude/Longitude coords.
*   **Weather and Telemetry Sliders**:
    *   Temperature (°C)
    *   Relative Humidity (%)
    *   Air Quality Index (PM2.5)
    *   Rainfall Lag (21d) — critical biological vector lag representing breeding cycles.
*   **Risk Metric Widgets**: Display six output channels formatted as percentage gauges.

### 2.2 Tab 2: Historical Trends Explorer
Visual telemetry interface to compare past recorded data trends.
*   **Filters**: Dropdowns to select specific dates, regions, or disease metrics.
*   **Interactive Maps/Charts**: Integrates mapping tools (e.g., Folium/Matplotlib) to show hot-spots and historical infection trajectories.

### 2.3 Tab 3: GenAI Clinical Advisory Desk
A dedicated space offering conversational analysis specifically targeted toward healthcare professionals.
*   **Scope**: Uses clinical parameters to write diagnostic/preventative reports.
*   **Tab Exclusivity**: The general consumer-facing footer ("Ask Rishi") is dynamically disabled on this tab to maintain focus on clinical telemetry.

### 2.4 Tab 4: Simulation Logs Archive
An operational logging ledger built on a local transactional SQLite database.
*   **Logging Trigger**: Action button allowing users to record the current sliders' state as a persistent scenario row.
*   **Data Table View**: Displays past scenarios with percentage-risk formatting and diagnostic color highlights.
*   **CSV Export**: Offers a one-click download option (`viralwell_simulation_report.csv`) of all stored simulation records.

### 2.5 Tab 5: Advanced ML Analytics
Deeper insights into the predictive machine learning engine.
*   **Feature Importance**: Renders relative weights of model variables (e.g., how humidity vs. rainfall lag affects malaria risk).
*   **Feature Explanations**: Educational tooltips illustrating why specific delay lags matter.

### 2.6 "Ask Rishi" Botanical Advisory Footer
A conversational agent offering natural and Ayurvedic support, positioned at the bottom of the layout.
*   **Scope**: Dynamic, consumer-friendly chat input widget.
*   **Tab Presence**: Automatically appears on all dashboard pages **except** Tab 3 (GenAI Clinical Desk).
*   **Meditation Spinner**: Custom UI progress overlay stating *"Rishi is in deep silent meditation. Please seek your remedy in a few moments."* during processing.

---

## 3. UI/UX Design System: "Cyber-Ayurvedic" Style Guide

ViralWell utilizes a custom-themed visual design to match a natural, Ayurvedic aesthetic.

*   **App Root Gradient**: Deep Obsidian Forest green theme (`#010704`).
*   **Visual Accent Layer (Background)**: An immersive, low-brightness dark forest canvas.
*   **Floating 3D Leaf Drift Animation**:
    *   **Types**: Confined to `🍃` (leaf fluttering in wind) and `🌿` (herb/sprig).
    *   **Drifting Channels**: Leaves drift vertically from top to bottom ONLY on the outer sides (0%–14% and 84%–96% screen width) to avoid cluttering core metrics.
    *   **Glow**: Soft bio-luminescent glow.
*   **Panels and Components**: Neumorphic Glass Cards utilizing `rgba(3, 15, 9, 0.6)` background, `20px` backdrop-blur, and green borders.

---

## 4. Technical Architecture

*   **Frontend & Layout**: Streamlit (Python) incorporating HTML overlays and `streamlit.components.v1` elements.
*   **Local Database**: SQLite (`sqlite3`) storing telemetry inputs and simulation predictions.
*   **Inference Engine**: Preserved ML predictions (Random Forest/Decision Tree/Linear models packaged in joblib formats).
*   **Generative AI Interface**: Integration layer requesting response text from active language models.

---

## 5. Security & Constraints
*   **Separation of Logic & Presentation**: Zero alteration of backend state variables, ML scoring weights, or database telemetry configurations.
*   **Legal Protections**: Global disclaimer bar fixed to viewport bottom reminding users that the dashboard is for educational/simulation purposes only.
