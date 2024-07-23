"use client";

import {
  Button,
  Image,
  Link,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Navbar as NextUiNavbar,
} from "@nextui-org/react";
import { usePathname, useRouter } from "next/navigation";
import { BiPlus } from "react-icons/bi";
import ThemeSwitcher from "./theme-switcher";

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  return (
    <NextUiNavbar className="border-b border-foreground" maxWidth="xl">
      <NavbarBrand>
        <Image src="/logotype.svg" alt="Hoppipolla" width={200} />
      </NavbarBrand>
      <NavbarContent className="hidden sm:flex gap-4" justify="center">
        <NavbarItem isActive={pathname.includes("policies")}>
          <Link
            color={pathname.includes("policies") ? "primary" : "foreground"}
            href="/policies"
          >
            Policies
          </Link>
        </NavbarItem>
        <NavbarItem isActive={pathname.includes("network")}>
          <Link
            color={pathname.includes("network") ? "primary" : "foreground"}
            href="/network"
          >
            Network
          </Link>
        </NavbarItem>
        <NavbarItem isActive={pathname.includes("data")}>
          <Link
            color={pathname.includes("data") ? "primary" : "foreground"}
            href="/data"
          >
            Data
          </Link>
        </NavbarItem>
      </NavbarContent>
      <NavbarContent justify="end">
        <NavbarItem>
          <Button
            color="primary"
            onClick={() => router.push("/policies/new")}
            endContent={<BiPlus />}
          >
            Create Policy
          </Button>
        </NavbarItem>
        <NavbarItem>
          <ThemeSwitcher />
        </NavbarItem>
      </NavbarContent>
    </NextUiNavbar>
  );
}
