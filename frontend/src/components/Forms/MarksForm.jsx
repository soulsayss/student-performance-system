import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Upload, FileText } from 'lucide-react';
import toast from 'react-hot-toast';

const MarksForm = ({ students, onSubmit }) => {
  const [uploadMethod, setUploadMethod] = useState('manual');
  const [csvFile, setCsvFile] = useState(null);
  const { register, handleSubmit, formState: { errors } } = useForm();

  const handleFormSubmit = async (data) => {
    try {
      if (uploadMethod === 'csv' && csvFile) {
        const formData = new FormData();
        formData.append('file', csvFile);
        await onSubmit(formData);
      } else {
        await onSubmit(data);
      }
      toast.success('Marks uploaded successfully!');
    } catch (error) {
      toast.error('Failed to upload marks');
    }
  };

  return (
    <div className="bg-white dark:bg-dark-bg-secondary rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-dark-text-primary mb-4 transition-colors duration-200">Upload Marks</h3>
      
      {/* Method Selection */}
      <div className="flex space-x-4 mb-6">
        <button
          type="button"
          onClick={() => setUploadMethod('manual')}
          className={`flex-1 py-2 px-4 rounded-lg border-2 transition-colors ${
            uploadMethod === 'manual'
              ? 'border-blue-600 bg-blue-50 dark:bg-blue-900/20 text-blue-600'
              : 'border-gray-300 dark:border-gray-600 text-gray-700 dark:text-dark-text-secondary hover:border-gray-400 dark:hover:border-gray-500'
          }`}
        >
          <FileText className="h-5 w-5 mx-auto mb-1" />
          Manual Entry
        </button>
        <button
          type="button"
          onClick={() => setUploadMethod('csv')}
          className={`flex-1 py-2 px-4 rounded-lg border-2 transition-colors ${
            uploadMethod === 'csv'
              ? 'border-blue-600 bg-blue-50 dark:bg-blue-900/20 text-blue-600'
              : 'border-gray-300 dark:border-gray-600 text-gray-700 dark:text-dark-text-secondary hover:border-gray-400 dark:hover:border-gray-500'
          }`}
        >
          <Upload className="h-5 w-5 mx-auto mb-1" />
          CSV Upload
        </button>
      </div>

      <form onSubmit={handleSubmit(handleFormSubmit)}>
        {uploadMethod === 'manual' ? (
          <>
            {/* Student Select */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-2 transition-colors duration-200">
                Student
              </label>
              <select
                {...register('student_id', { required: 'Student is required' })}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              >
                <option value="">Select student</option>
                {students?.map((student) => (
                  <option key={student.student_id} value={student.student_id}>
                    {student.roll_number} - {student.name}
                  </option>
                ))}
              </select>
              {errors.student_id && (
                <p className="mt-1 text-sm text-red-600">{errors.student_id.message}</p>
              )}
            </div>

            {/* Subject */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-2 transition-colors duration-200">
                Subject
              </label>
              <input
                type="text"
                {...register('subject', { required: 'Subject is required' })}
                placeholder="e.g., Mathematics"
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              />
              {errors.subject && (
                <p className="mt-1 text-sm text-red-600">{errors.subject.message}</p>
              )}
            </div>

            {/* Exam Type */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-2 transition-colors duration-200">
                Exam Type
              </label>
              <select
                {...register('exam_type', { required: 'Exam type is required' })}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              >
                <option value="">Select exam type</option>
                <option value="quiz">Quiz</option>
                <option value="midterm">Midterm</option>
                <option value="final">Final</option>
                <option value="assignment">Assignment</option>
              </select>
              {errors.exam_type && (
                <p className="mt-1 text-sm text-red-600">{errors.exam_type.message}</p>
              )}
            </div>

            {/* Marks */}
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-2 transition-colors duration-200">
                  Marks Obtained
                </label>
                <input
                  type="number"
                  {...register('score', { 
                    required: 'Marks obtained is required',
                    min: { value: 0, message: 'Must be 0 or greater' }
                  })}
                  placeholder="0"
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
                />
                {errors.score && (
                  <p className="mt-1 text-sm text-red-600">{errors.score.message}</p>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-2 transition-colors duration-200">
                  Total Marks
                </label>
                <input
                  type="number"
                  {...register('max_score', { 
                    required: 'Total marks is required',
                    min: { value: 1, message: 'Must be greater than 0' }
                  })}
                  placeholder="100"
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
                />
                {errors.max_score && (
                  <p className="mt-1 text-sm text-red-600">{errors.max_score.message}</p>
                )}
              </div>
            </div>

            {/* Exam Date */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-2 transition-colors duration-200">
                Exam Date
              </label>
              <input
                type="date"
                {...register('exam_date', { required: 'Exam date is required' })}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              />
              {errors.exam_date && (
                <p className="mt-1 text-sm text-red-600">{errors.exam_date.message}</p>
              )}
            </div>
          </>
        ) : (
          <>
            {/* CSV Upload */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-2 transition-colors duration-200">
                Upload CSV File
              </label>
              <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center hover:border-blue-500 dark:hover:border-blue-400 transition-colors">
                <Upload className="h-12 w-12 mx-auto text-gray-400 dark:text-gray-500 mb-2" />
                <input
                  type="file"
                  accept=".csv"
                  onChange={(e) => setCsvFile(e.target.files[0])}
                  className="hidden"
                  id="marks-csv-upload"
                />
                <label
                  htmlFor="marks-csv-upload"
                  className="cursor-pointer text-blue-600 hover:text-blue-700 font-medium"
                >
                  Choose CSV file
                </label>
                {csvFile && (
                  <p className="mt-2 text-sm text-gray-600 dark:text-dark-text-secondary transition-colors duration-200">{csvFile.name}</p>
                )}
              </div>
              <p className="mt-2 text-xs text-gray-500 dark:text-dark-text-secondary transition-colors duration-200">
                Format: student_id, subject, exam_type, score, max_score, exam_date
              </p>
            </div>
          </>
        )}

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          Upload Marks
        </button>
      </form>
    </div>
  );
};

export default MarksForm;
