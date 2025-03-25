import React from 'react';
import JsonTable from './JsonTable';
import 'antd/dist/reset.css';

const App = () => {
  // Here, we're using static data; in production, you'd fetch your JSON output from your API.
  const data = [
    {
      "from_page": "https://example.com/about",
      "src": "https://example.com/images/logo.png",
      "alt": null,
      "status": 200,
      "is_duplicate": true,
      "used_on_pages": [
        "https://example.com",
        "https://example.com/about",
        "https://example.com/team"
      ]
    },
    {
      "from_page": "https://example.com/about",
      "src": "https://example.com/images/missing.jpg",
      "alt": "Broken Image",
      "status": 404,
      "is_duplicate": false,
      "used_on_pages": [
        "https://example.com/about"
      ]
    }
  ];

  return (
    <div style={{ padding: 24 }}>
      <h2>SEO Analyzer Dashboard</h2>
      <JsonTable data={data} />
    </div>
  );
};

export default App;
