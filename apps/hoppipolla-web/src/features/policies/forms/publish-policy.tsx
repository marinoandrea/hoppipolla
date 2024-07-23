"use client";

import { Policy } from "@/services/policy-manager/service";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Button,
  Input,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  Textarea,
} from "@nextui-org/react";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

interface IPublishPolicyFormProps {
  publishAction(data: FormValues): Promise<Policy>;
}

const schema = z.object({
  // TODO: issuer selection
  title: z.string().optional(),
  description: z.string().optional(),
  statements: z.string(),
});

type FormValues = z.infer<typeof schema>;

export default function PublishPolicyForm(props: IPublishPolicyFormProps) {
  const [serviceError, setServiceError] = useState<string>();

  const router = useRouter();

  const form = useForm({
    mode: "onSubmit",
    resolver: zodResolver(schema),
    defaultValues: {
      title: "",
      description: "",
      statements: "",
    },
  });

  async function onSubmit(data: FormValues) {
    try {
      const policy = await props.publishAction(data);
      router.replace(`/policies/${policy.id}`);
    } catch (e) {
      setServiceError(new String(e).toString());
    }
  }

  return (
    <form
      className="flex flex-col gap-4"
      onSubmit={form.handleSubmit(onSubmit)}
    >
      <Input
        type="text"
        label="Title"
        isInvalid={!!form.formState.errors.title}
        errorMessage={form.formState.errors.title?.message}
        placeholder="Example Policy"
        {...form.register("title")}
        isRequired
      />
      <Textarea
        label="Description"
        isInvalid={!!form.formState.errors.description}
        errorMessage={form.formState.errors.description?.message}
        placeholder="This is an example policy"
        {...form.register("description")}
        isRequired
      />
      <Textarea
        label="Statements"
        isInvalid={!!form.formState.errors.statements}
        errorMessage={form.formState.errors.statements?.message}
        placeholder="valid(Path) :- path(Path)."
        {...form.register("statements")}
        isRequired
      />

      <div className="flex justify-end">
        <Button
          color="primary"
          type="submit"
          isLoading={form.formState.isSubmitting}
          onClick={form.handleSubmit(onSubmit)}
        >
          Publish
        </Button>
      </div>

      {serviceError && (
        <Modal
          isOpen={!!serviceError}
          onOpenChange={(isOpen) =>
            setServiceError(isOpen ? serviceError : undefined)
          }
        >
          <ModalContent>
            {(onClose) => (
              <>
                <ModalHeader className="flex flex-col gap-1">Error</ModalHeader>
                <ModalBody>
                  <p>{serviceError}</p>
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
      )}
    </form>
  );
}
