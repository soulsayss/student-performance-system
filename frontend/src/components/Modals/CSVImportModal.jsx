import { useState } from 'react';
import { X, Upload, Download, AlertCircle, CheckCircle, XCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import adminService from '../../services/adminService.new';

const CSVImportModal = ({ isOpen, onClose, onSuccess }) => {
  const [selectedType, setSelectedType] = useState('students');
  const [selectedFile, setSelectedFile] = useState(null);
  const [clearExisting, setClearExisting] = useState(false);
  const [importing, setImporting] = useState(false);
  const [results, setResults] = useState(null);

  const dataTypes = [
    { value: 'students', label: 'Students', description: 'Import student records' },
    { value: 'teachers', label: 'Teachers', description: 'Import teacher records' },
    { value: 'parents', label: 'Parents', description: 'Import parent records' },
    { value: 'marks', label: 'Marks', description: 'Import exam marks' },
    { value: 'attendance', label: 'Attendance', description: 'Import attendance records' }
  ];

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.name.endsWith('.csv')) {
        toast.error('Please select a CSV file');
        return;
      }
      setSelectedFile(file);
      setResults(null);
    }
  };

  const handleDownloadTemplate = async () => {
    try {
      await adminService.downloadCSVTemplate(selectedType);
      toast.success('Template downloaded successfully');
    } catch (error) {
      toast.error('Failed to download template');
    }
  };

  const handleImport = async () => {
    if (!selectedFile) {
      toast.error('Please select a file');
      return;
    }

    if (clearExisting) {
      const confirmed = window.confirm(
        `WARNING: This will delete all existing ${selectedType} data. Are you sure?`
      );
      if (!confirmed) return;
    }

    try {
      setImporting(true);
      const response = await adminService.importCSVData(
        selectedFile,
        selectedType,
        clearExisting
      );

      setResults(response);

      if (response.success && response.imported_count > 0) {
        toast.success(`Successfully imported ${response.imported_count} records`);
        if (onSuccess) onSuccess();
      } else if (response.errors && response.errors.length > 0) {
        toast.error('Import completed with errors. Check results below.');
      }
    } catch (error) {
      toast.error('Failed to import data');
      setResults({
        success: false,
        imported_count: 0,
        errors: [error.response?.data?.message || error.message || 'Unknown error'],
        skipped: []
      });
    } finally {
      setImporting(false);
    }
  };

  const handleClose = () => {
    setSelectedFile(null);
    setResults(null);
    setClearExisting(false);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-dark-bg-secondary rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto transition-colors duration-200">
        {/* Header */}
        <div className="sticky top-0 bg-white dark:bg-dark-bg-secondary border-b border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">
                Import Data from CSV
              </h2>
              <p className="text-sm text-gray-600 dark:text-dark-text-secondary mt-1 transition-colors duration-200">
                Upload CSV files to bulk import data into the system
              </p>
            </div>
            <button
              onClick={handleClose}
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
            >
              <X className="h-6 w-6" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Data Type Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-3 transition-colors duration-200">
              Select Data Type
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {dataTypes.map((type) => (
                <button
                  key={type.value}
                  onClick={() => {
                    setSelectedType(type.value);
                    setSelectedFile(null);
                    setResults(null);
                  }}
                  className={`p-4 rounded-lg border-2 text-left transition-all ${
                    selectedType === type.value
                      ? 'border-blue-600 bg-blue-50 dark:bg-blue-900/20'
                      : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
                  }`}
                >
                  <div className="font-semibold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">
                    {type.label}
                  </div>
                  <div className="text-xs text-gray-600 dark:text-dark-text-secondary mt-1 transition-colors duration-200">
                    {type.description}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Download Template */}
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 transition-colors duration-200">
            <div className="flex items-start space-x-3">
              <AlertCircle className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm text-blue-900 dark:text-blue-200 mb-2 transition-colors duration-200">
                  Download the CSV template to ensure correct format
                </p>
                <button
                  onClick={handleDownloadTemplate}
                  className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                >
                  <Download className="h-4 w-4" />
                  <span>Download {selectedType} Template</span>
                </button>
              </div>
            </div>
          </div>

          {/* File Upload */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-2 transition-colors duration-200">
              Upload CSV File
            </label>
            <div 
              onClick={() => document.getElementById('csv-file-input').click()}
              className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center hover:border-blue-500 dark:hover:border-blue-400 transition-colors cursor-pointer"
            >
              <Upload className="h-12 w-12 mx-auto text-gray-400 dark:text-gray-500 mb-3" />
              <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="hidden"
                id="csv-file-input"
              />
              <span className="text-blue-600 hover:text-blue-700 font-medium cursor-pointer">
                Choose CSV file
              </span>
              {selectedFile && (
                <p className="mt-2 text-sm text-gray-600 dark:text-dark-text-secondary transition-colors duration-200">
                  ✓ Selected: {selectedFile.name}
                </p>
              )}
            </div>
          </div>

          {/* Clear Existing Option */}
          <div className="flex items-start space-x-3 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg transition-colors duration-200">
            <input
              type="checkbox"
              id="clear-existing"
              checked={clearExisting}
              onChange={(e) => setClearExisting(e.target.checked)}
              className="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded"
            />
            <label htmlFor="clear-existing" className="flex-1">
              <span className="block text-sm font-medium text-gray-900 dark:text-dark-text-primary transition-colors duration-200">
                Clear existing data before import
              </span>
              <span className="block text-xs text-yellow-800 dark:text-yellow-200 mt-1 transition-colors duration-200">
                WARNING: This will permanently delete all existing {selectedType} data
              </span>
            </label>
          </div>

          {/* Results */}
          {results && (
            <div className="space-y-3">
              {/* Summary */}
              <div className={`p-4 rounded-lg border-2 ${
                results.success && results.imported_count > 0
                  ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
                  : 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
              } transition-colors duration-200`}>
                <div className="flex items-start space-x-3">
                  {results.success && results.imported_count > 0 ? (
                    <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                  ) : (
                    <XCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
                  )}
                  <div className="flex-1">
                    <p className={`text-sm font-medium ${
                      results.success && results.imported_count > 0
                        ? 'text-green-900 dark:text-green-200'
                        : 'text-red-900 dark:text-red-200'
                    } transition-colors duration-200`}>
                      {results.message || `Imported ${results.imported_count} records`}
                    </p>
                  </div>
                </div>
              </div>

              {/* Errors */}
              {results.errors && results.errors.length > 0 && (
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 transition-colors duration-200">
                  <h4 className="text-sm font-semibold text-red-900 dark:text-red-200 mb-2 transition-colors duration-200">
                    Errors ({results.errors.length})
                  </h4>
                  <div className="max-h-40 overflow-y-auto space-y-1">
                    {results.errors.map((error, idx) => (
                      <p key={idx} className="text-xs text-red-800 dark:text-red-300 transition-colors duration-200">
                        • {error}
                      </p>
                    ))}
                  </div>
                </div>
              )}

              {/* Skipped */}
              {results.skipped && results.skipped.length > 0 && (
                <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 transition-colors duration-200">
                  <h4 className="text-sm font-semibold text-yellow-900 dark:text-yellow-200 mb-2 transition-colors duration-200">
                    Skipped ({results.skipped.length})
                  </h4>
                  <div className="max-h-40 overflow-y-auto space-y-1">
                    {results.skipped.map((skip, idx) => (
                      <p key={idx} className="text-xs text-yellow-800 dark:text-yellow-300 transition-colors duration-200">
                        • {skip}
                      </p>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-50 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 p-6 flex justify-end space-x-3 transition-colors duration-200">
          <button
            onClick={handleClose}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-dark-text-secondary hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            Close
          </button>
          <button
            onClick={handleImport}
            disabled={!selectedFile || importing}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            {importing ? (
              <>
                <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
                <span>Importing...</span>
              </>
            ) : (
              <>
                <Upload className="h-4 w-4" />
                <span>Import Data</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default CSVImportModal;
