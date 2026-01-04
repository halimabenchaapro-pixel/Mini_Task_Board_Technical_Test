import Modal from './Modal';
import Button from './Button';

const DeleteConfirmation = ({ isOpen, onClose, onConfirm, taskTitle }) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Delete Task">
      <div className="space-y-4">
        <p className="text-gray-700">
          Are you sure you want to delete the task <strong>"{taskTitle}"</strong>? This action
          cannot be undone.
        </p>

        <div className="flex gap-3 pt-4">
          <Button variant="danger" onClick={onConfirm} className="flex-1">
            Delete
          </Button>
          <Button variant="secondary" onClick={onClose} className="flex-1">
            Cancel
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export default DeleteConfirmation;
