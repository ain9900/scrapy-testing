import React from 'react';
import { Table } from 'antd';

const JsonTable = ({ data }) => {
  if (!data || data.length === 0) return <p>No data to display</p>;

  const columns = Object.keys(data[0]).map((key) => ({
    title: key,
    dataIndex: key,
    key: key,
    render: (text) =>
      Array.isArray(text)
        ? text.join(', ')
        : typeof text === 'object'
        ? JSON.stringify(text)
        : text
  }));

  return (
    <Table
      columns={columns}
      dataSource={data.map((item, i) => ({ ...item, key: i }))}
      pagination={{ pageSize: 10 }}
      bordered
    />
  );
};

export default JsonTable;
