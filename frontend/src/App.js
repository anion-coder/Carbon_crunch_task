import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
  LinearProgress,
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

function App() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      const extension = file.name.split('.').pop().toLowerCase();
      if (['js', 'jsx', 'py'].includes(extension)) {
        setFile(file);
        setError(null);
      } else {
        setError('Please upload a .js, .jsx, or .py file');
        setFile(null);
      }
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/javascript': ['.js', '.jsx'],
      'text/x-python': ['.py'],
    },
    multiple: false,
  });

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/analyze-code`, formData);
      setAnalysis(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error analyzing code');
    } finally {
      setLoading(false);
    }
  };

  const renderScoreBar = (label, score, maxScore) => (
    <Box sx={{ mb: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
        <Typography variant="body2">{label}</Typography>
        <Typography variant="body2">{score}/{maxScore}</Typography>
      </Box>
      <LinearProgress
        variant="determinate"
        value={(score / maxScore) * 100}
        sx={{ height: 8, borderRadius: 4 }}
      />
    </Box>
  );

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Code Quality Analyzer
      </Typography>

      <Paper
        {...getRootProps()}
        sx={{
          p: 3,
          mb: 4,
          textAlign: 'center',
          cursor: 'pointer',
          bgcolor: isDragActive ? 'action.hover' : 'background.paper',
          border: '2px dashed',
          borderColor: isDragActive ? 'primary.main' : 'grey.300',
        }}
      >
        <input {...getInputProps()} />
        <Typography variant="body1">
          {isDragActive
            ? 'Drop the file here'
            : 'Drag and drop a file here, or click to select'}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          Supported formats: .js, .jsx, .py
        </Typography>
      </Paper>

      {file && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1">
            Selected file: {file.name}
          </Typography>
          <button
            onClick={handleAnalyze}
            disabled={loading}
            style={{
              padding: '8px 16px',
              backgroundColor: '#1976d2',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? <CircularProgress size={20} /> : 'Analyze Code'}
          </button>
        </Box>
      )}

      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}

      {analysis && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Analysis Results
          </Typography>
          <Typography variant="h4" color="primary" gutterBottom>
            Overall Score: {analysis.overall_score}/100
          </Typography>

          <Box sx={{ my: 3 }}>
            {renderScoreBar('Naming Conventions', analysis.breakdown.naming, 10)}
            {renderScoreBar('Modularity', analysis.breakdown.modularity, 20)}
            {renderScoreBar('Comments', analysis.breakdown.comments, 20)}
            {renderScoreBar('Formatting', analysis.breakdown.formatting, 15)}
            {renderScoreBar('Reusability', analysis.breakdown.reusability, 15)}
            {renderScoreBar('Best Practices', analysis.breakdown.best_practices, 20)}
          </Box>

          <Divider sx={{ my: 2 }} />

          <Typography variant="h6" gutterBottom>
            Recommendations
          </Typography>
          <List>
            {analysis.recommendations.map((rec, index) => (
              <ListItem key={index}>
                <ListItemText primary={rec} />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}
    </Container>
  );
}

export default App; 