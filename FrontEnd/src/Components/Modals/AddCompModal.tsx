import { Modal } from "flowbite-react";
import AddCompanyForm from "../Forms/AddCompanyForm";

interface AddCompModal {
  show: boolean;
  switchState: (show: boolean) => void;
}

const AddCompModal = (props: AddCompModal) => {
  return (
    <Modal
      show={props.show}
      onClose={() => props.switchState(false)}
      size="xl"
      className="w-full"
    >
      <Modal.Header>Добавить организацию</Modal.Header>
      <Modal.Body>
        <AddCompanyForm onCloseModalAction={props.switchState} />
      </Modal.Body>
    </Modal>
  );
};

export default AddCompModal;
