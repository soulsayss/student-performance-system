import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Upload, Calendar, Users } from 'lucide-react';
import toast from 'react-hot-toast';

const AttendanceForm = ({ students, onSubmit }) => {
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
        // For manual entry, send each student separately
        const studentIds = Array.isArray(data.student_ids) 
          ? data.student_ids 
          : [data.student_ids];
        
        // Send attendance for each selected student
        for (const studentId of studentIds) {
          await onSubmit({
            student_id: parseInt(studentId),
            date: data.date,
            status: data.status
          });
        }
      }
      toast.success('Attendance uploaded successfully!');
    } catch (error) {
      toast.error('Failed to upload attendance');
    }
  };

  return (
    <div className="bg-white dark:bg-dark-bg-secondary rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-dark-text-primary mb-4 transition-colors duration-200">Upload Attendance</h3>
      
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
          <Users className="h-5 w-5 mx-auto mb-1" />
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
            {/* Date Picker */}
            <div className="mb-4">
              <label htmlFor="attendance-date" className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-2 transition-colors duration-200">
                <Calendar className="inline h-4 w-4 mr-1" />
                Date
              </label>
              <input
                id="attendance-date"
                type="date"
                {...register('date', { required: 'Date is required' })}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              />
              {errors.date && (
                <p className="mt-1 text-sm text-red-600">{errors.date.message}</p>
              )}
            </div>

            {/* Student Select */}
            <div className="mb-4">
              <label htmlFor="attendance-students" className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-2 transition-colors duration-200">
                Students
              </label>
              <select
                id="attendance-students"
                multiple
                {...register('student_ids', { required: 'Select at least one student' })}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent h-32 bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              >
                {students?.map((student) => (
                  <option key={student.student_id} value={student.student_id}>
                    {student.roll_number} - {student.name}
                  </option>
                ))}
              </select>
              {errors.student_ids && (
                <p className="mt-1 text-sm text-red-600">{errors.student_ids.message}</p>
              )}
              <p className="mt-1 text-xs text-gray-500 dark:text-dark-text-secondary transition-colors duration-200">Hold Ctrl/Cmd to select multiple</p>
            </div>

            {/* Status Dropdown */}
            <div className="mb-4">
              <label htmlFor="attendance-status" className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-2 transition-colors duration-200">
                Status
              </label>
              <select
                id="attendance-status"
                {...register('status', { required: 'Status is required' })}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              >
                <option value="">Select status</option>
                <option value="present">Present</option>
                <option value="absent">Absent</option>
                <option value="late">Late</option>
              </select>
              {errors.status && (
                <p className="mt-1 text-sm text-red-600">{errors.status.message}</p>
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
                  id="csv-upload"
                />
                <label
                  htmlFor="csv-upload"
                  className="cursor-pointer text-blue-600 hover:text-blue-700 font-medium"
                >
                  Choose CSV file
                </label>
                {csvFile && (
                  <p className="mt-2 text-sm text-gray-600 dark:text-dark-text-secondary transition-colors duration-200">{csvFile.name}</p>
                )}
              </div>
              <p className="mt-2 text-xs text-gray-500 dark:text-dark-text-secondary transition-colors duration-200">
                Format: date, student_id, status
              </p>
            </div>
          </>
        )}

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          Upload Attendance
        </button>
      </form>
    </div>
  );
};

export default AttendanceForm;
