// frontend/src/AnalyzeForm.jsx

import React, { useState } from 'react';
import { Input, Button, message } from 'antd';

const AnalyzeForm = () => {
  const [url, setUrl] = useState('');
  const [taskId, setTaskId] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!url) {
      message.error('Please enter a URL');
      return;
    }
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/analyze/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      const data = await response.json();
      if (data.task_id) {
        setTaskId(data.task_id);
        message.success('Analysis started. Task ID: ' + data.task_id);
      } else {
        message.error('Unexpected response from API');
      }
    } catch (err) {
      message.error('Error: ' + err.message);
    }
    setLoading(false);
  };

  return (
    <div style={{ marginBottom: 24 }}>
      <Input
        placeholder="Enter web address (e.g., https://example.com)"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ width: 300, marginRight: 8 }}
      />
      <Button type="primary" onClick={handleAnalyze} loading={loading}>
        Analyze
      </Button>
      {taskId && (
        <div style={{ marginTop: 16 }}>
          <strong>Task ID:</strong> {taskId}
        </div>
      )}
    </div>
  );
};

export default AnalyzeForm;
