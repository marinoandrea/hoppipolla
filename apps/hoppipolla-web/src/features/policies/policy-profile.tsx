"use client";

import {
  Button,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow,
  Textarea,
} from "@nextui-org/react";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { BiEdit, BiTrash } from "react-icons/bi";

import { deletePolicy } from "@/actions/policies";
import { Policy } from "@/services/policy-manager/service";

interface IPolicyProfileProps {
  policy: Policy;
}

export default function PolicyProfile({ policy }: IPolicyProfileProps) {
  const router = useRouter();
  return (
    <div className="flex flex-col gap-4">
      <Table>
        <TableHeader>
          <TableColumn>Attribute</TableColumn>
          <TableColumn>Value</TableColumn>
        </TableHeader>
        <TableBody>
          <TableRow key="title">
            <TableCell>Title</TableCell>
            <TableCell>{policy.title}</TableCell>
          </TableRow>
          <TableRow key="id">
            <TableCell>ID</TableCell>
            <TableCell className="font-mono">{policy.id}</TableCell>
          </TableRow>
          <TableRow key="createdAt">
            <TableCell>Created</TableCell>
            <TableCell>{policy.createdAt.toLocaleString()}</TableCell>
          </TableRow>
          <TableRow key="updatedAt">
            <TableCell>Updated</TableCell>
            <TableCell>{policy.updatedAt.toLocaleString()}</TableCell>
          </TableRow>
          <TableRow key="issuer">
            <TableCell>Active</TableCell>
            <TableCell className="text-secondary">
              {policy.active ? "true" : "false"}
            </TableCell>
          </TableRow>
          <TableRow key="issuer">
            <TableCell>Issuer</TableCell>
            <TableCell>{policy.issuer.name}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
      <Textarea
        isReadOnly
        minRows={50}
        label="Description"
        value={policy.description}
      />
      <Textarea
        isReadOnly
        minRows={50}
        label="Statements"
        value={policy.statements}
      />

      <div className="flex justify-end items-center gap-4">
        <Button
          onClick={() => router.push(`/policies/${policy.id}/update`)}
          endContent={<BiEdit />}
        >
          Edit
        </Button>
        <DeletePolicyButton policy={policy} />
      </div>
    </div>
  );
}

function DeletePolicyButton({ policy }: { policy: Policy }) {
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [deletionError, setDeletionError] = useState<string>();

  const router = useRouter();

  return (
    <>
      <Button
        color="danger"
        onClick={() => setIsDeleteModalOpen(true)}
        endContent={<BiTrash />}
      >
        Delete
      </Button>

      <Modal isOpen={isDeleteModalOpen} onOpenChange={setIsDeleteModalOpen}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">Error</ModalHeader>
              <ModalBody>
                <p>Are you sure you want to delete policy {policy.title}?</p>
              </ModalBody>
              <ModalFooter>
                <Button onClick={onClose}>Cancel</Button>
                <Button
                  color="danger"
                  isLoading={isDeleting}
                  onPress={async () => {
                    setIsDeleting(true);
                    try {
                      await deletePolicy(policy.id);
                      router.replace("/policies");
                      router.refresh();
                    } catch (e) {
                      setDeletionError(new String(e).toString());
                    } finally {
                      setIsDeleting(false);
                      onClose();
                    }
                  }}
                >
                  Delete
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>

      <Modal
        isOpen={!!deletionError}
        onOpenChange={(isOpen) =>
          setDeletionError(isOpen ? deletionError : undefined)
        }
      >
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">Error</ModalHeader>
              <ModalBody>
                <p>{deletionError}</p>
              </ModalBody>
              <ModalFooter>
                <Button color="primary" onPress={onClose}>
                  Ok
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
}
