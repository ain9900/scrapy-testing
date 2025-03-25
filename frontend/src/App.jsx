// frontend/src/App.jsx

import React from 'react';
import AnalyzeForm from './AnalyzeForm';
import 'antd/dist/reset.css';

const App = () => {
  return (
    <div style={{ padding: 24 }}>
      <h2>SEO Analyzer Dashboard</h2>
      <AnalyzeForm />
      {/* You can later add a table or results view here */}
    </div>
  );
};

export default App;
