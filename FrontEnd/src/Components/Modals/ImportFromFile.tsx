import { Modal } from "flowbite-react";
import { UploadFileForm } from "../Forms/UploadFileForm"

interface UploadFileModalProps {
  show: boolean;
  switchState: (show: boolean) => void;
}

const UploadFileModal = (props: UploadFileModalProps) => {
  return (
    <Modal
      show={props.show}
      onClose={() => props.switchState(false)}
      size="xl"
      className="w-full"
    >
      <Modal.Header>Загрузить файл</Modal.Header>
      <Modal.Body>
        <UploadFileForm />
      </Modal.Body>
    </Modal>
  );
};

export default UploadFileModal;