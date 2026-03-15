import { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import toast from 'react-hot-toast';

const ResourceModal = ({ isOpen, onClose, onSave, resource = null }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    subject: '',
    link: '',
    resource_type: 'article',
    difficulty: 'beginner'
  });

  useEffect(() => {
    if (resource) {
      setFormData({
        title: resource.title || '',
        description: resource.description || '',
        subject: resource.subject || '',
        link: resource.link || '',
        resource_type: resource.resource_type || 'article',
        difficulty: resource.difficulty || 'beginner'
      });
    } else {
      setFormData({
        title: '',
        description: '',
        subject: '',
        link: '',
        resource_type: 'article',
        difficulty: 'beginner'
      });
    }
  }, [resource, isOpen]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.title || !formData.subject || !formData.link) {
      toast.error('Title, subject, and link are required');
      return;
    }

    try {
      await onSave(formData);
      onClose();
    } catch (error) {
      console.error('Error saving resource:', error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-dark-bg-secondary rounded-lg p-6 w-full max-w-md transition-colors duration-200">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">
            {resource ? 'Edit Resource' : 'Add New Resource'}
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors">
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-1 transition-colors duration-200">
              Title *
            </label>
            <input
              id="title"
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              required
            />
          </div>

          <div>
            <label htmlFor="subject" className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-1 transition-colors duration-200">
              Subject *
            </label>
            <input
              id="subject"
              type="text"
              value={formData.subject}
              onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              required
              placeholder="e.g., Mathematics, Physics"
            />
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-1 transition-colors duration-200">
              Description
            </label>
            <textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              rows="3"
            />
          </div>

          <div>
            <label htmlFor="link" className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-1 transition-colors duration-200">
              Link/URL *
            </label>
            <input
              id="link"
              type="url"
              value={formData.link}
              onChange={(e) => setFormData({ ...formData, link: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              required
              placeholder="https://..."
            />
          </div>

          <div>
            <label htmlFor="resource_type" className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-1 transition-colors duration-200">
              Type *
            </label>
            <select
              id="resource_type"
              value={formData.resource_type}
              onChange={(e) => setFormData({ ...formData, resource_type: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              required
            >
              <option value="video">Video</option>
              <option value="article">Article</option>
              <option value="pdf">PDF</option>
              <option value="quiz">Quiz</option>
            </select>
          </div>

          <div>
            <label htmlFor="difficulty" className="block text-sm font-medium text-gray-700 dark:text-dark-text-secondary mb-1 transition-colors duration-200">
              Difficulty *
            </label>
            <select
              id="difficulty"
              value={formData.difficulty}
              onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              required
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-dark-text-secondary hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              {resource ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ResourceModal;
