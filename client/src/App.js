import { Suspense } from "react";
import { Layout } from "antd";
import ReactGA from "react-ga4";
import { CircularProgress, Grid } from "@mui/material";
import Sidebar from "./components/sidebar";
import NavBar from "./components/navbar";
import Container from "./components/container";
import { SnackbarProvider } from "notistack";
import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { useRecoilState, useRecoilValue } from "recoil";
import { isMobileState, profileFlagsState } from "./data/atoms";

const menuItems = [
  {
    key: "4",
    label: "Apps",
    link: "/",
  },
  {
    key: "1",
    label: "Playground",
    link: "/playground",
  },
  {
    key: "6",
    label: "Discover",
    link: "/hub",
  },
  {
    key: "2",
    label: "Endpoints",
    link: "/endpoint",
  },
  {
    key: "7",
    label: "Data",
    link: "/data",
  },
  {
    key: "3",
    label: "History",
    link: "/history",
  },
  {
    key: "5",
    label: "Settings",
    link: "/settings",
  },
];

export default function App({ children }) {
  const location = useLocation();

  useEffect(() => {
    ReactGA.initialize("G-WV60HC9CHD");
    ReactGA.send({
      hitType: "pageview",
      page: location.pathname + location.search,
      title: location.pathname,
    });
  }, [location]);

  const [isMobile, setIsMobile] = useRecoilState(isMobileState);
  const profileFlags = useRecoilValue(profileFlagsState);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 900);
    };

    window.addEventListener("resize", handleResize);

    // Cleanup
    return () => window.removeEventListener("resize", handleResize);
  }, [setIsMobile]);

  return (
    <div id="app-container">
      <SnackbarProvider
        maxSnack={3}
        autoHideDuration={3000}
        anchorOrigin={{ horizontal: "center", vertical: "top" }}
      />
      {isMobile && (
        <NavBar
          menuItems={[
            ...menuItems,
            {
              key: "9",
              label: "Docs",
              link: "https://docs.trypromptly.com",
            },
          ].concat(
            profileFlags.IS_ORGANIZATION_OWNER
              ? [
                  {
                    key: "8",
                    label: "Organization",
                    link: "/organization",
                  },
                ]
              : [],
          )}
        />
      )}
      <Layout style={{ height: "100vh" }}>
        {!isMobile && (
          <Sidebar
            menuItems={menuItems.concat(
              profileFlags.IS_ORGANIZATION_OWNER
                ? [
                    {
                      key: "8",
                      label: "Organization",
                      link: "/organization",
                    },
                  ]
                : [],
            )}
          />
        )}
        <Suspense
          fallback={
            <Grid
              sx={{
                margin: "auto",
              }}
            >
              <CircularProgress />
            </Grid>
          }
        >
          <Container>{children}</Container>
        </Suspense>
      </Layout>
      <div
        dangerouslySetInnerHTML={{
          __html:
            '<promptly-app-embed published-app-id="f4d7cb50-1805-4add-80c5-e30334bce53c" width="100px" chat-bubble="true"></promptly-app-embed>',
        }}
      ></div>
    </div>
  );
}
